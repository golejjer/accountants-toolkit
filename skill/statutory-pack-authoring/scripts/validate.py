#!/usr/bin/env python3
"""Statutory pack checker (schema 0.1).

Usage: python validate.py <pack-folder>

Checks the manifest, the rule data, the guidance file, and recomputes every
worked example from the rules. Exit code 0 when there are no errors.
Needs Python 3.8+ and PyYAML (pip install pyyaml).
"""
import re
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from fractions import Fraction
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is needed: pip install pyyaml")

SUBTYPES = {"current_asset", "non_current_asset", "current_liability", "non_current_liability",
            "equity", "operating_income", "non_operating_income", "cost_of_sales",
            "operating_expense", "non_operating_expense"}
STANDARD_ACCOUNTS = {"trade_receivables", "trade_payables", "revenue", "expense", "bank"}
KINDS = {"output_input", "levy", "withholding"}
SIDES_BY_KIND = {"output_input": {"sales", "purchases"}, "levy": {"sales"},
                 "withholding": {"receipts", "payments"}}
TREATMENTS_BY_KIND = {
    "output_input": {"standard", "reduced", "zero_rated", "exempt", "out_of_scope", "reverse_charge"},
    "levy": {"standard", "reduced", "exempt", "out_of_scope"},
    "withholding": {"withholding"},
}
RATED = {"standard", "reduced", "zero_rated", "reverse_charge", "withholding"}
FREQUENCIES = {"monthly", "quarterly", "half_yearly", "yearly"}
MEASURES = {"net", "output_tax", "input_tax", "tax", "withheld"}
DOCUMENTS = {"sale_invoice": "sales", "purchase_bill": "purchases",
             "receipt": "receipts", "payment": "payments"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"ERROR   {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"WARNING {where}: {msg}")


def dec(value, rep, where, what):
    if isinstance(value, float):
        rep.err(where, f"{what} must be a quoted string, not a number ({value!r})")
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        rep.err(where, f"{what} is not a number: {value!r}")
        return None


def frac(value, rep, where):
    try:
        f = Fraction(str(value))
        if f <= 0 or f > 1:
            rep.err(where, f"base fraction {value!r} must be above 0 and at most 1")
        return f
    except (ValueError, ZeroDivisionError):
        rep.err(where, f"base fraction {value!r} is not a fraction like \"2/3\" or \"0.5\"")
        return None


def as_date(value, rep, where, what, required=True):
    if value is None:
        if required:
            rep.err(where, f"{what} is missing")
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        rep.err(where, f"{what} {value!r} is not a date YYYY-MM-DD")
        return None


def load(path, rep):
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except FileNotFoundError:
        rep.err(path.name, "file is missing")
    except yaml.YAMLError as exc:
        rep.err(path.name, f"not valid YAML: {exc}")
    return None


class Pack:
    def __init__(self, folder, rep):
        self.folder, self.rep = folder, rep
        self.manifest = load(folder / "pack.yaml", rep) or {}
        self.rules = load(folder / "rules.yaml", rep) or {}
        self.questions, self.accounts, self.taxes, self.codes = {}, {}, {}, {}
        self.decimals, self.level = 2, "line"

    # ---------- conditions ----------
    def check_condition(self, cond, where):
        if cond is None:
            return
        if isinstance(cond, str):
            q = self.questions.get(cond)
            if not q:
                self.rep.err(where, f"condition refers to unknown question {cond!r}")
            elif q.get("type") != "yes_no":
                self.rep.err(where, f"question {cond!r} is not yes_no; use {{question, in: [...]}}")
        elif isinstance(cond, dict):
            q = self.questions.get(cond.get("question"))
            if not q:
                self.rep.err(where, f"condition refers to unknown question {cond.get('question')!r}")
            elif q.get("type") != "choice":
                self.rep.err(where, "a {question, in} condition needs a choice question")
            else:
                bad = set(cond.get("in") or []) - set(q.get("options") or [])
                if bad or not cond.get("in"):
                    self.rep.err(where, f"condition options {sorted(bad) or '[]'} are not options of {cond['question']!r}")
        else:
            self.rep.err(where, f"condition {cond!r} is not understood")

    @staticmethod
    def holds(cond, answers):
        if cond is None:
            return True
        if isinstance(cond, str):
            return answers.get(cond) is True
        return answers.get(cond.get("question")) in (cond.get("in") or [])

    # ---------- structure ----------
    def check_manifest(self):
        rep, m = self.rep, self.manifest
        if str(m.get("schema_version")) != "0.1":
            rep.err("pack.yaml", "schema_version must be \"0.1\"")
        p = m.get("pack") or {}
        if not ID_RE.match(str(p.get("id", ""))):
            rep.err("pack.yaml", "pack.id must be lowercase letters, digits and hyphens")
        if not re.match(r"^[A-Z]{2}$", str(p.get("jurisdiction", ""))):
            rep.err("pack.yaml", "pack.jurisdiction must be a two-letter ISO country code")
        if not re.match(r"^[A-Z]{3}$", str(p.get("currency", ""))):
            rep.err("pack.yaml", "pack.currency must be a three-letter ISO currency code")
        if not VERSION_RE.match(str(p.get("version", ""))):
            rep.err("pack.yaml", "pack.version must look like 1.2.3")
        if p.get("level") not in {"private", "shared", "verified"}:
            rep.err("pack.yaml", "pack.level must be private, shared or verified")
        if not p.get("authors"):
            rep.err("pack.yaml", "at least one author is required")
        authors = {a.get("name") for a in p.get("authors") or []}
        for r in p.get("reviewers") or []:
            if r.get("name") in authors:
                rep.err("pack.yaml", f"{r.get('name')!r} cannot be both author and reviewer")
        if p.get("level") == "verified" and not p.get("reviewers"):
            rep.warn("pack.yaml", "a verified pack needs a reviewer before release")

    def check_rules(self):
        rep, r = self.rep, self.rules
        for q in r.get("questions") or []:
            k = q.get("key")
            if not k or k in self.questions:
                rep.err("questions", f"missing or duplicate key {k!r}")
                continue
            self.questions[k] = q
            if q.get("type") not in {"yes_no", "choice"}:
                rep.err(f"questions.{k}", "type must be yes_no or choice")
            if q.get("type") == "choice" and not q.get("options"):
                rep.err(f"questions.{k}", "a choice question needs options")
            if not q.get("text"):
                rep.err(f"questions.{k}", "text is missing")

        for a in r.get("accounts") or []:
            k = a.get("key")
            if not k or k in self.accounts or k in STANDARD_ACCOUNTS:
                rep.err("accounts", f"missing, duplicate or reserved key {k!r}")
                continue
            self.accounts[k] = a
            if a.get("subtype") not in SUBTYPES:
                rep.err(f"accounts.{k}", f"subtype {a.get('subtype')!r} is not one of the fixed subtypes")
            if not a.get("name"):
                rep.err(f"accounts.{k}", "name is missing")
            self.check_condition(a.get("add_when"), f"accounts.{k}.add_when")

        need = {"output_input": ["output", "input"], "withholding": ["receivable", "payable"]}
        for t in r.get("taxes") or []:
            k, where = t.get("key"), f"taxes.{t.get('key')}"
            if not k or k in self.taxes:
                rep.err("taxes", f"missing or duplicate key {k!r}")
                continue
            self.taxes[k] = t
            kind = t.get("kind")
            if kind not in KINDS:
                rep.err(where, f"kind must be one of {sorted(KINDS)}")
                continue
            accts = t.get("accounts") or {}
            required = list(need.get(kind, ["payable"]))
            if kind == "levy":
                if t.get("charged_to_customer") not in (True, False):
                    rep.err(where, "a levy needs charged_to_customer: true or false")
                elif t.get("charged_to_customer") is False:
                    required.append("expense")
            for role in required:
                if accts.get(role) not in self.accounts:
                    rep.err(where, f"accounts.{role} must name an account in the accounts section")
            self.check_condition(t.get("applies_when"), f"{where}.applies_when")
            f = t.get("filing")
            if kind != "withholding" or f:
                if not f or f.get("frequency") not in FREQUENCIES:
                    rep.err(where, f"filing.frequency must be one of {sorted(FREQUENCIES)}")
                elif not isinstance(f.get("due"), dict) or not (
                        set(f["due"]) & {"days_after_period_end", "day_of_following_month"}):
                    rep.err(where, "filing.due needs days_after_period_end or day_of_following_month")
            th = t.get("registration_threshold")
            if th:
                dec(th.get("amount"), rep, where, "registration_threshold.amount")
                as_date(th.get("effective_from"), rep, where, "registration_threshold.effective_from")
                if not th.get("source"):
                    rep.warn(where, "registration_threshold has no source")

        for c in r.get("tax_codes") or []:
            self.check_code(c)
        self.check_cycles()

        rd = r.get("rounding") or {}
        if rd.get("level") not in {"line", "document"}:
            rep.err("rounding", "level must be line or document")
        if rd.get("method") != "half_up":
            rep.err("rounding", "method must be half_up in schema 0.1")
        if not isinstance(rd.get("decimals"), int) or not 0 <= rd.get("decimals") <= 4:
            rep.err("rounding", "decimals must be a whole number from 0 to 4")
        self.decimals, self.level = rd.get("decimals", 2), rd.get("level", "line")

        fed = set()
        self.boxes = {}
        for ret in r.get("returns") or []:
            rk = ret.get("key")
            if ret.get("tax") not in self.taxes:
                rep.err(f"returns.{rk}", "tax must name a tax")
            keys = set()
            self.boxes[rk] = ret.get("boxes") or []
            for b in self.boxes[rk]:
                bk, where = str(b.get("key")), f"returns.{rk}.box {b.get('key')}"
                if bk in keys:
                    rep.err(where, "duplicate box key")
                keys.add(bk)
                for s in b.get("sum") or []:
                    code = self.codes.get(s.get("code"))
                    if not code:
                        rep.err(where, f"unknown code {s.get('code')!r}")
                        continue
                    fed.add(s["code"])
                    if s.get("side") not in set(code.get("applies_to") or []):
                        rep.err(where, f"side {s.get('side')!r} is not in {s['code']}'s applies_to")
                    if s.get("measure") not in MEASURES:
                        rep.err(where, f"measure must be one of {sorted(MEASURES)}")
                if not b.get("sum"):
                    rep.err(where, "box has nothing to sum")
        for k, c in self.codes.items():
            if c.get("treatment") != "out_of_scope" and k not in fed:
                rep.err(f"tax_codes.{k}", "does not feed any return box")

        for p in r.get("pending_changes") or []:
            if not p.get("description") or not p.get("source"):
                rep.err("pending_changes", "each entry needs a description and a source")

    def check_code(self, c):
        rep, k = self.rep, c.get("key")
        where = f"tax_codes.{k}"
        if not k or k in self.codes:
            rep.err("tax_codes", f"missing or duplicate key {k!r}")
            return
        self.codes[k] = c
        tax = self.taxes.get(c.get("tax"))
        if not tax:
            rep.err(where, f"tax {c.get('tax')!r} is not defined")
            return
        kind, treatment = tax.get("kind"), c.get("treatment")
        if treatment not in TREATMENTS_BY_KIND.get(kind, set()):
            rep.err(where, f"treatment {treatment!r} is not allowed for a {kind} tax")
        sides = set(c.get("applies_to") or [])
        if not sides or not sides <= SIDES_BY_KIND.get(kind, set()):
            rep.err(where, f"applies_to must be from {sorted(SIDES_BY_KIND.get(kind, set()))}")
        if treatment == "reverse_charge" and sides != {"purchases"}:
            rep.err(where, "a reverse charge code applies to purchases only")
        if "input_recoverable" in c and c["input_recoverable"] not in (True, False):
            rep.err(where, "input_recoverable must be true or false")
        if "purchases" in sides and kind == "output_input" and treatment in RATED and "input_recoverable" not in c:
            rep.err(where, "say whether input tax is recoverable (input_recoverable)")
        for t in c.get("compound_on") or []:
            if t not in self.taxes:
                rep.err(where, f"compound_on names unknown tax {t!r}")
            if t == c.get("tax"):
                rep.err(where, "a code cannot compound on its own tax")
        self.check_condition(c.get("applies_when"), f"{where}.applies_when")
        rates = c.get("rates") or []
        if treatment in RATED and not rates:
            rep.err(where, f"a {treatment} code needs rates")
        if treatment not in RATED and rates:
            rep.err(where, f"a {treatment} code has no rates")
        spans = []
        for i, r in enumerate(rates):
            w = f"{where}.rates[{i}]"
            rate = dec(r.get("rate"), rep, w, "rate")
            if rate is not None:
                if treatment == "zero_rated" and rate != 0:
                    rep.err(w, "a zero_rated code must have rate \"0\"")
                if treatment != "zero_rated" and not (0 < rate < 100):
                    rep.err(w, "rate must be above 0 and below 100 (percent)")
            base = r.get("base") or {}
            if set(base) - {"fraction", "gross_up"}:
                rep.err(w, "base may only contain fraction and gross_up")
            if "fraction" in base:
                frac(base["fraction"], rep, w)
            if "gross_up" in base and base["gross_up"] not in (True, False):
                rep.err(w, "gross_up must be true or false")
            start = as_date(r.get("effective_from"), rep, w, "effective_from")
            end = as_date(r.get("effective_to"), rep, w, "effective_to", required=False)
            if start and end and end < start:
                rep.err(w, "effective_to is before effective_from")
            if not r.get("source"):
                rep.err(w, "every rate needs a source")
            if start:
                spans.append((start, end or date.max, i))
        spans.sort()
        for a, b in zip(spans, spans[1:]):
            if b[0] <= a[1]:
                rep.err(where, f"rates[{a[2]}] and rates[{b[2]}] overlap in time")

    def check_cycles(self):
        graph = {}
        for c in self.codes.values():
            graph.setdefault(c.get("tax"), set()).update(c.get("compound_on") or [])
        state = {}

        def visit(n, path):
            if state.get(n) == 1:
                self.rep.err("tax_codes", f"compound_on loop: {' -> '.join(path + [n])}")
                return
            if state.get(n) == 2:
                return
            state[n] = 1
            for m in graph.get(n, ()):
                visit(m, path + [n])
            state[n] = 2
        for n in list(graph):
            visit(n, [])

    # ---------- engine ----------
    def rate_on(self, code, when):
        for r in code.get("rates") or []:
            start = as_date(r.get("effective_from"), self.rep, "", "", required=False)
            end = as_date(r.get("effective_to"), self.rep, "", "", required=False) or date.max
            if start and start <= when <= end:
                base = r.get("base") or {}
                return (Decimal(str(r["rate"])), Fraction(str(base.get("fraction", "1"))),
                        bool(base.get("gross_up")))
        return None

    def q(self, amount):
        return amount.quantize(Decimal(1).scaleb(-self.decimals), rounding=ROUND_HALF_UP)

    def charged(self, code, side):
        """Is this code's tax added to the amount owed by or to the other party?"""
        tax = self.taxes[code["tax"]]
        t = code.get("treatment")
        if tax["kind"] == "output_input":
            return t in {"standard", "reduced", "zero_rated"}
        if tax["kind"] == "levy":
            return side == "sales" and tax.get("charged_to_customer") is True and t in {"standard", "reduced"}
        return False

    def line_taxes(self, net, codes, when, rounded):
        """Taxes on one line, in dependency order. net may be unrounded."""
        by_tax = {self.codes[c]["tax"]: c for c in codes}
        order, seen = [], set()

        def place(tax_key):
            if tax_key in seen or tax_key not in by_tax:
                return
            seen.add(tax_key)
            for dep in self.codes[by_tax[tax_key]].get("compound_on") or []:
                place(dep)
            order.append(tax_key)
        for t in by_tax:
            place(t)
        amounts, out = {}, {}
        for t in order:
            code = self.codes[by_tax[t]]
            info = self.rate_on(code, when) if code.get("treatment") in RATED else None
            if info is None:
                out[by_tax[t]] = Decimal(0)
                amounts[t] = Decimal(0)
                continue
            rate, fraction, gross_up = info
            base = net * Decimal(fraction.numerator) / Decimal(fraction.denominator)
            base += sum((amounts.get(d, Decimal(0)) for d in code.get("compound_on") or []), Decimal(0))
            tax = base * rate / (Decimal(100) - rate) if gross_up else base * rate / Decimal(100)
            if rounded:
                tax = self.q(tax)
            out[by_tax[t]] = tax
            amounts[t] = tax
        return out

    def compute(self, ex, where):
        rep = self.rep
        when = as_date(ex.get("date"), rep, where, "date")
        side = DOCUMENTS.get(ex.get("document"))
        if not when or not side:
            if not side:
                rep.err(where, f"document must be one of {sorted(DOCUMENTS)}")
            return None
        answers = ex.get("answers") or {}
        for k, v in answers.items():
            q = self.questions.get(k)
            if not q:
                rep.err(where, f"answer to unknown question {k!r}")
            elif q["type"] == "choice" and v not in (q.get("options") or []):
                rep.err(where, f"answer {v!r} is not an option of {k!r}")
        for k in self.questions:
            if k not in answers:
                rep.warn(where, f"no answer given to question {k!r}")

        def usable(code_key):
            c = self.codes.get(code_key)
            if not c:
                rep.err(where, f"unknown tax code {code_key!r}")
                return False
            if side not in (c.get("applies_to") or []):
                rep.err(where, f"{code_key} does not apply to {side}")
                return False
            if not self.holds(self.taxes[c["tax"]].get("applies_when"), answers) or not self.holds(c.get("applies_when"), answers):
                rep.err(where, f"{code_key} does not apply to a business with these answers")
                return False
            if c.get("treatment") in RATED and self.rate_on(c, when) is None:
                rep.err(where, f"{code_key} has no rate in force on {when}")
                return False
            return True

        post, boxes = {}, {}

        def dr(acct, amt):
            post[acct] = post.get(acct, Decimal(0)) + amt

        def feed(code_key, measure, amt):
            for rk, bxs in self.boxes.items():
                for b in bxs:
                    for s in b.get("sum") or []:
                        if s.get("code") == code_key and s.get("side") == side and s.get("measure") == measure:
                            boxes.setdefault(rk, {})
                            boxes[rk][str(b["key"])] = boxes[rk].get(str(b["key"]), Decimal(0)) + amt

        result = {"lines": []}
        if side in {"receipts", "payments"}:
            st = ex.get("settlement") or {}
            amount = dec(st.get("amount"), rep, where, "settlement.amount")
            if amount is None:
                return None
            withheld = Decimal(0)
            for ck in st.get("codes") or []:
                if not usable(ck):
                    return None
                rate, fraction, gross_up = self.rate_on(self.codes[ck], when)
                base = amount * Decimal(fraction.numerator) / Decimal(fraction.denominator)
                w = self.q(base * rate / (Decimal(100) - rate) if gross_up else base * rate / Decimal(100))
                withheld += w
                accts = self.taxes[self.codes[ck]["tax"]]["accounts"]
                dr(accts["receivable"], w) if side == "receipts" else dr(accts["payable"], -w)
                feed(ck, "withheld", w)
                feed(ck, "net", amount)
            if side == "receipts":
                dr("bank", amount - withheld)
                dr("trade_receivables", -amount)
            else:
                dr("trade_payables", amount)
                dr("bank", -(amount - withheld))
            result["total"] = amount - withheld
            result["postings"], result["boxes"] = post, boxes
            return result

        lines = ex.get("lines") or []
        if not lines:
            rep.err(where, "an invoice or bill needs lines")
            return None
        doc_level = self.level == "document"
        raw = []  # (net, {code: unrounded or rounded tax}, codes)
        for i, ln in enumerate(lines):
            lw = f"{where}.lines[{i}]"
            codes = ln.get("codes") or []
            if not all(usable(c) for c in codes):
                return None
            taxes_seen = [self.codes[c]["tax"] for c in codes]
            if len(taxes_seen) != len(set(taxes_seen)):
                rep.err(lw, "a line can carry only one code per tax")
                return None
            amt = dec(ln.get("amount"), rep, lw, "amount")
            if amt is None:
                return None
            if ln.get("amount_type") == "inclusive":
                if any(self.codes[c].get("treatment") == "reverse_charge" for c in codes):
                    rep.err(lw, "an inclusive amount cannot carry a reverse charge code")
                    return None
                unit = self.line_taxes(Decimal(1), codes, when, rounded=False)
                m = Decimal(1) + sum((v for c, v in unit.items() if self.charged(self.codes[c], side)), Decimal(0))
                net_est = amt / m
                if doc_level:
                    raw.append((net_est, self.line_taxes(net_est, codes, when, False), codes, amt))
                else:
                    taxes = self.line_taxes(net_est, codes, when, True)
                    charged = sum((v for c, v in taxes.items() if self.charged(self.codes[c], side)), Decimal(0))
                    raw.append((amt - charged, taxes, codes, amt))
            elif ln.get("amount_type") == "exclusive":
                taxes = self.line_taxes(amt, codes, when, rounded=not doc_level)
                raw.append((amt, taxes, codes, None))
            else:
                rep.err(lw, "amount_type must be exclusive or inclusive")
                return None

        totals = {}
        for net, taxes, codes, gross in raw:
            for c, v in taxes.items():
                totals[c] = totals.get(c, Decimal(0)) + v
        if doc_level:
            totals = {c: self.q(v) for c, v in totals.items()}
            charged_total = sum((v for c, v in totals.items() if self.charged(self.codes[c], side)), Decimal(0))
            if all(g is not None for *_, g in raw):
                net_total = sum((g for *_, g in raw), Decimal(0)) - charged_total
            elif all(g is None for *_, g in raw):
                net_total = sum((n for n, *_ in raw), Decimal(0))
            else:
                rep.err(where, "with document rounding, lines must be all inclusive or all exclusive")
                return None
            nets = [self.q(n) for n, *_ in raw]
            nets[-1] += net_total - sum(nets, Decimal(0))
        else:
            nets = [n for n, *_ in raw]
            net_total = sum(nets, Decimal(0))
        for i, (n, taxes, codes, _) in enumerate(raw):
            entry = {"net": nets[i]}
            if not doc_level:
                entry["taxes"] = taxes
            result["lines"].append(entry)
            for c in codes:
                feed(c, "net", nets[i])
        result["tax_totals"] = totals

        charged_sum = Decimal(0)
        expense_extra = Decimal(0)
        for c, v in totals.items():
            code, tax = self.codes[c], self.taxes[self.codes[c]["tax"]]
            accts, t = tax.get("accounts") or {}, code.get("treatment")
            if self.charged(code, side):
                charged_sum += v
            if tax["kind"] == "output_input" and t in {"standard", "reduced", "zero_rated"}:
                if side == "sales":
                    dr(accts["output"], -v)
                    feed(c, "output_tax", v)
                elif code.get("input_recoverable"):
                    dr(accts["input"], v)
                    feed(c, "input_tax", v)
                else:
                    expense_extra += v
            elif t == "reverse_charge":
                dr(accts["output"], -v)
                feed(c, "output_tax", v)
                if code.get("input_recoverable"):
                    dr(accts["input"], v)
                    feed(c, "input_tax", v)
                else:
                    expense_extra += v
            elif tax["kind"] == "levy" and t in {"standard", "reduced"}:
                dr(accts["payable"], -v)
                if tax.get("charged_to_customer") is False:
                    dr(accts["expense"], v)
                feed(c, "tax", v)
        total = net_total + charged_sum
        if side == "sales":
            dr("trade_receivables", total)
            dr("revenue", -net_total)
        else:
            dr("expense", net_total + expense_extra)
            dr("trade_payables", -total)
        result["total"], result["postings"], result["boxes"] = total, post, boxes
        if sum(post.values(), Decimal(0)) != 0:
            rep.err(where, "internal check: postings do not balance")
        for acct in post:
            if acct not in STANDARD_ACCOUNTS and not self.holds(self.accounts[acct].get("add_when"), answers):
                rep.err(where, f"posts to {acct}, which is not added for a business with these answers")
        return result

    # ---------- examples ----------
    def check_examples(self):
        folder = self.folder / "examples"
        files = sorted(folder.glob("*.yaml")) if folder.is_dir() else []
        if not files:
            self.rep.err("examples", "no worked examples found")
            return
        per_code = {}
        for f in files:
            ex = load(f, self.rep)
            if not ex:
                continue
            where = f"examples/{f.name}"
            if not str(ex.get("working") or "").strip():
                self.rep.err(where, "working is missing: show the hand calculation")
            got = self.compute(ex, where)
            if got is None:
                continue
            for ln in ex.get("lines") or []:
                for c in ln.get("codes") or []:
                    per_code[c] = per_code.get(c, 0) + 1
            for c in (ex.get("settlement") or {}).get("codes") or []:
                per_code[c] = per_code.get(c, 0) + 1
            self.compare(ex.get("expected") or {}, got, where)
        for c in self.codes:
            n = per_code.get(c, 0)
            if n < 3:
                self.rep.warn(f"tax_codes.{c}", f"has {n} worked example(s); at least 3 are expected")

    def compare(self, exp, got, where):
        rep = self.rep

        def same(a, b, what):
            ea = dec(a, rep, where, what) if a is not None else None
            if ea is None or ea != b:
                rep.err(where, f"{what}: expected {a}, rules give {b}")

        same(exp.get("total"), got["total"], "total")
        exp_lines = exp.get("lines") or []
        if got["lines"]:
            if len(exp_lines) != len(got["lines"]):
                rep.err(where, "expected.lines does not match the number of lines")
            for i, (e, g) in enumerate(zip(exp_lines, got["lines"])):
                same(e.get("net"), g["net"], f"line {i + 1} net")
                if "taxes" in g:
                    for c, v in g["taxes"].items():
                        same((e.get("taxes") or {}).get(c), v, f"line {i + 1} {c}")
            if self.level == "document":
                for c, v in got["tax_totals"].items():
                    same((exp.get("tax_totals") or {}).get(c), v, f"tax total {c}")
        exp_post = {}
        for p in exp.get("postings") or []:
            if ("debit" in p) == ("credit" in p):
                rep.err(where, f"posting to {p.get('account')} needs exactly one of debit or credit")
                continue
            amt = dec(p.get("debit", p.get("credit")), rep, where, "posting amount")
            if amt is None:
                continue
            exp_post[p.get("account")] = exp_post.get(p.get("account"), Decimal(0)) + (amt if "debit" in p else -amt)
        for acct in set(exp_post) | {a for a, v in got["postings"].items() if v != 0}:
            e, g = exp_post.get(acct, Decimal(0)), got["postings"].get(acct, Decimal(0))
            if e != g:
                fmt = lambda v: f"debit {v}" if v >= 0 else f"credit {-v}"
                rep.err(where, f"posting {acct}: expected {fmt(e)}, rules give {fmt(g)}")
        exp_boxes = exp.get("boxes") or {}
        keys = {(r, str(b)) for r, bx in exp_boxes.items() for b in (bx or {})}
        keys |= {(r, b) for r, bx in got["boxes"].items() for b, v in bx.items() if v != 0}
        for r, b in sorted(keys):
            e = (exp_boxes.get(r) or {}).get(b, (exp_boxes.get(r) or {}).get(int(b)) if b.isdigit() else None)
            g = got["boxes"].get(r, {}).get(b, Decimal(0))
            same(e if e is not None else "0", g, f"{r} box {b}")

    # ---------- guidance ----------
    def check_guidance(self):
        path = self.folder / "guidance" / "GUIDANCE.md"
        if not path.exists():
            self.rep.err("guidance", "guidance/GUIDANCE.md is missing")
            return
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            self.rep.err("guidance", "front matter (name, description) is missing")
        else:
            fm = yaml.safe_load(m.group(1)) or {}
            if not ID_RE.match(str(fm.get("name", ""))) or len(str(fm.get("name", ""))) > 64:
                self.rep.err("guidance", "name must be lowercase with hyphens, up to 64 characters")
            if not fm.get("description") or len(str(fm.get("description"))) > 1024:
                self.rep.err("guidance", "description is missing or longer than 1,024 characters")
        if len(text.splitlines()) > 500:
            self.rep.warn("guidance", "longer than 500 lines; move detail to guidance/references/")
        checks = [
            (r"\b\d+(\.\d+)?\s?%", "contains a percentage; the guidance must not carry rates to compute with"),
            (r"\b(multiply|divide|times|formula)\b", "looks like a calculation instruction"),
            (r"\b(compliant|guaranteed|approved|official)\b", "contains a compliance claim word"),
            (r"\b(ignore|disregard|override)\b.{0,40}\b(instruction|rule|previous|system)", "looks like an instruction to change the assistant's rules"),
            (r"\b(send|email|forward|upload|post)\b.{0,60}\b(to|at)\b.{0,40}(@|https?://)", "looks like an instruction to send data somewhere"),
            (r"\b(password|card number|bank account number|national id)\b", "mentions collecting sensitive personal data"),
        ]
        for n, (pattern, msg) in enumerate(checks):
            for i, line in enumerate(text.splitlines(), 1):
                if re.search(pattern, line, re.I):
                    # the last three patterns are refused by the platform's safety check
                    (self.rep.err if n >= 3 else self.rep.warn)(f"guidance line {i}", msg)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1])
    rep = Report()
    pack = Pack(folder, rep)
    pack.check_manifest()
    pack.check_rules()
    if not rep.errors:
        pack.check_examples()
    else:
        rep.warn("examples", "not recomputed until the rule errors above are fixed")
    pack.check_guidance()
    for path in ("CHANGELOG.md", "README.md"):
        if not (folder / path).exists():
            rep.warn(path, "file is missing")
    for line in rep.errors + rep.warnings:
        print(line)
    print(f"\n{len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    sys.exit(1 if rep.errors else 0)


if __name__ == "__main__":
    main()

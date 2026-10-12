# Writing the guidance file

`guidance/GUIDANCE.md` is read by business owners' AI assistants while they record sales, purchases and settlements. It tells the assistant **how to think and what to ask**, never **what to compute**.

## Contents

1. **When this pack applies:** which businesses, which taxes, from which date.
2. **Choosing a tax code:** for each code, plain signs that a sale or purchase belongs to it, and the questions to ask when it is not obvious. Example: "If the customer is outside the country and the service is used outside it, ask whether it is an exported service before choosing the zero-rated code."
3. **Common mistakes:** what businesses typically get wrong, and how to spot it.
4. **Registration and thresholds:** what to tell a business approaching a threshold. The platform supplies the figures; the guidance explains what they mean.
5. **Filing calendar:** what is due and when, in words. The platform computes the dates.
6. **What a return needs:** which records and documents the business should keep.
7. **Where to read more:** links to the authority's own pages, with the date checked.

## Rules

- **No figures to compute with.** Never write "multiply by 15%" or a formula. Refer to "the tax the platform calculates".
- **Speak to the assistant, briefly.** Short sections and plain sentences. Keep the file under 500 lines; put long material in a `guidance/references/` file and link it.
- **Ask, don't assume.** Where a choice depends on facts, tell the assistant what to ask the business.
- **Cite.** Each rule names its legal source and date.
- **No instructions outside the subject.** The guidance must not tell an assistant to use other tools, contact anyone, visit or send data to any address, change its own rules, adopt a persona, or collect personal information. The platform's safety check refuses any pack that does.
- **No client data.** Use invented names and amounts in examples.
- **No compliance claims.** Never "compliant", "guaranteed", "approved" or "official".
- **Same front matter as a skill:** a `name` (lowercase, hyphens, up to 64 characters) and a `description` (what it covers and when to use it, up to 1,024 characters).

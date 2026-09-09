# -*- coding: utf-8 -*-
"""Content source for the practice-area pages.

STATUS: DRAFT. Every legal statement below needs review by J. Hutchins before
launch. Georgia code references are included so they can be checked quickly.
"""

FIRM = {
    "name": "Jay Hutch Law",
    "phone_display": "855-488-2452",
    "phone_link": "+18554882452",
    "email": "contact@jayhutchlaw.com",
    "base": "https://www.jayhutchlaw.com",
}

HUB = {
    "title": "Practice Areas | Atlanta Attorney | Jay Hutch Law",
    "description": "Jay Hutch Law represents clients across Georgia in personal injury, DUI defense, premises liability, immigration, estate planning, and traffic citations.",
    "h1": "Clear counsel for life's legal challenges.",
    "lede": "Practical solutions and personal attention, so you understand your options and can move forward with confidence. Select an area below to read more about how the firm approaches it.",
}

PAGES = [
    {
        "slug": "personal-injury",
        "num": "01",
        "nav": "Personal Injury",
        "title": "Atlanta Personal Injury Lawyer | Georgia Injury Claims | Jay Hutch Law",
        "description": "Injured in Georgia because of someone else's negligence? Jay Hutch Law helps clients pursue compensation for medical bills, lost income, and pain and suffering. Free consultation.",
        "h1": "Personal Injury",
        "lede": "Representation for people injured because of another person or company's negligence — with attention to the deadlines and evidence that decide these cases.",
        "source": "practice_personal_injury",
        "sections": [
            ("What these cases involve", [
                "A personal injury claim arises when someone is hurt because another party failed to act with reasonable care. That covers vehicle collisions, injuries on unsafe property, and harm caused by a business's negligence.",
                "The claim is not only about the injury itself. It covers the medical expenses that follow, the income lost while unable to work, the cost of future treatment, and the pain and disruption the injury causes.",
            ]),
            ("Two Georgia rules that shape your claim", [
                "<strong>The two-year deadline.</strong> Georgia generally gives an injured person two years from the date of injury to file a personal injury lawsuit (O.C.G.A. § 9-3-33). Claims for property damage generally allow four years. Miss the deadline and the claim is usually barred no matter how strong it is.",
                "<strong>Shared fault.</strong> Georgia follows a modified comparative negligence rule (O.C.G.A. § 51-12-33). If you are found partly responsible, your recovery is reduced by your share of the fault — and if you are found 50 percent or more responsible, you recover nothing. This is why insurers work hard to assign you a portion of the blame, and why how fault is documented matters so much.",
            ]),
            ("How the firm approaches an injury claim", [
                "We start by understanding what happened and what it has cost you — medically, financially, and practically. From there we gather the evidence that establishes responsibility: incident reports, photographs, medical records, witness accounts, and where appropriate, expert analysis.",
                "We handle communication with the insurance carriers so you are not negotiating your own claim while recovering. Early offers frequently arrive before the full extent of an injury is understood, and accepting one usually closes the claim permanently.",
                "Most injury claims resolve through negotiation. Some do not, and preparing a claim properly from the beginning is what makes a strong negotiating position possible.",
            ]),
        ],
        "checklist": ("What to do after an injury", [
            "Get medical attention, and follow through on treatment",
            "Photograph the scene, the vehicles or hazard, and your injuries",
            "Get the names and contact details of any witnesses",
            "Report the incident, and keep a copy of the report",
            "Keep every bill, receipt, and record of missed work",
            "Speak to an attorney before giving a recorded statement",
        ]),
        "faqs": [
            ("How long do I have to file a personal injury claim in Georgia?",
             "Georgia generally allows two years from the date of injury for a personal injury lawsuit, and four years for property damage. Some circumstances shorten or extend that window — claims against a government entity, for example, carry much earlier notice requirements. Because the deadline is strict, it is worth confirming yours early rather than close to the date."),
            ("What if I was partly at fault?",
             "You may still recover. Georgia reduces your compensation by your percentage of fault, and bars recovery entirely if you are 50 percent or more responsible. How fault is assessed is often disputed, which is why the evidence gathered early matters."),
            ("Should I accept the insurance company's first offer?",
             "Not before you understand the full extent of your injury. Early offers often arrive before treatment is complete, and accepting one generally closes the claim for good — including for costs that have not yet appeared."),
            ("What does it cost to hire the firm for an injury case?",
             "Personal injury matters are commonly handled on a contingency basis, meaning the fee comes from the recovery rather than up front. We will explain the specific terms that would apply to your matter during your consultation."),
        ],
        "related": ["premises-liability", "dui-defense", "traffic-citations"],
    },
    {
        "slug": "dui-defense",
        "num": "02",
        "nav": "DUI Defense",
        "title": "Atlanta DUI Lawyer | Georgia DUI Defense Attorney | Jay Hutch Law",
        "description": "Charged with DUI in Georgia? Jay Hutch Law reviews the stop, the testing, and the license consequences. Act quickly — license deadlines run from the date of arrest. Free consultation.",
        "h1": "DUI Defense",
        "lede": "A DUI charge puts your licence, your record, and often your employment at stake. The details of how the stop and the testing were handled matter enormously.",
        "source": "practice_dui",
        "urgent": "A Georgia DUI arrest starts a separate clock on your driver's licence that runs independently of your criminal case — and it is short. Call <a href=\"tel:+18554882452\">855-488-2452</a> as soon as you can.",
        "sections": [
            ("Two cases, not one", [
                "A Georgia DUI arrest creates two separate proceedings. The first is the criminal case in court. The second is an administrative action against your driver's licence, handled by the Department of Driver Services.",
                "The administrative case moves first, and it has a short deadline that begins at arrest. Missing it can cost you your licence regardless of what later happens in court. This is the single most common and most costly mistake people make after a DUI arrest.",
            ]),
            ("What we examine", [
                "<strong>The stop.</strong> An officer needs a lawful reason to pull a vehicle over. If that basis does not hold up, what followed may be challenged.",
                "<strong>The field sobriety testing.</strong> These tests are standardised, and they are only meaningful when administered as designed. Conditions, instructions, and the officer's own observations are all reviewable.",
                "<strong>The chemical testing.</strong> Breath and blood testing depends on properly maintained equipment, correct procedure, and a valid chain of custody. Georgia's implied consent notice must also be read correctly and at the right time.",
                "<strong>The licence consequences.</strong> These vary with your age, your licence type, whether you have prior offences, and whether you submitted to or refused testing.",
            ]),
            ("What is at stake", [
                "Georgia sets the per se blood alcohol limit at 0.08 percent for most drivers, 0.04 percent for commercial licence holders, and 0.02 percent for drivers under 21. A driver can also be charged without meeting those thresholds.",
                "Beyond the immediate penalties, a DUI conviction stays on a Georgia driving record and can affect employment, insurance, and professional licensing for years. Understanding the whole picture — not just the court date — is part of deciding how to proceed.",
            ]),
        ],
        "checklist": ("After a DUI arrest", [
            "Note the exact date of arrest — licence deadlines run from it",
            "Keep every document you were given, including the citation",
            "Write down what you remember while it is fresh",
            "Do not discuss the arrest on social media",
            "Do not miss your court date, whatever else is happening",
            "Speak with an attorney before the licence deadline passes",
        ]),
        "faqs": [
            ("How soon do I need to act after a Georgia DUI arrest?",
             "Immediately. The administrative action against your driver's licence has a deadline that begins on the date of arrest, and it is measured in days, not weeks. It is separate from your court date. Call the office as soon as you are able so the deadline can be confirmed and protected."),
            ("Can I refuse a breath test in Georgia?",
             "You can refuse, but refusal carries its own licence consequences under Georgia's implied consent law, and the refusal itself may be raised in your case. Whether a refusal helps or hurts depends entirely on the circumstances, which is worth reviewing with an attorney rather than guessing."),
            ("Will a DUI stay on my record permanently?",
             "A DUI conviction in Georgia generally remains on your driving record and is not eligible for record restriction in the way some other offences are. This is a significant part of why the initial handling of the case matters."),
            ("Do I have to go to court?",
             "DUI charges generally require court appearances. Do not miss any date listed on your paperwork while waiting to hear from our office — a missed appearance creates a separate and more serious problem."),
        ],
        "related": ["traffic-citations", "personal-injury", "premises-liability"],
    },
    {
        "slug": "premises-liability",
        "num": "03",
        "nav": "Premises Liability",
        "title": "Atlanta Premises Liability Lawyer | Slip and Fall | Jay Hutch Law",
        "description": "Injured on unsafe property in Georgia? Jay Hutch Law handles slip-and-fall and other premises liability claims, investigating responsibility and pursuing compensation. Free consultation.",
        "h1": "Premises Liability",
        "lede": "When a property owner fails to keep a space reasonably safe and someone is hurt, the question becomes what the owner knew, and what they did about it.",
        "source": "practice_premises",
        "sections": [
            ("What counts as a premises liability claim", [
                "These claims arise when an unsafe condition on someone's property causes injury: a wet floor without warning, poor lighting in a stairwell, a broken handrail, an unmarked change in floor level, debris in a walkway, or inadequate security.",
                "Slip-and-fall incidents are the most familiar example, but the category is broader — it covers any preventable hazard a property owner or occupier should have addressed.",
            ]),
            ("The duty owners owe", [
                "Under Georgia law, a property owner or occupier owes a duty of ordinary care to keep the premises safe for people invited onto them (O.C.G.A. § 51-3-1). The level of duty depends on why you were there — a customer in a store is owed more than someone present without permission.",
                "The central question in most of these cases is knowledge. Did the owner know about the hazard, or should they reasonably have known? A spill that appeared moments earlier is treated differently from one that had been there for hours, or a broken step that had been reported repeatedly.",
                "That is also why these cases turn on evidence that disappears quickly. Surveillance footage is often overwritten within days, and a hazard is usually cleaned up immediately after an incident.",
            ]),
            ("How the firm handles these claims", [
                "We move to preserve evidence early — requesting footage before it is recycled, identifying maintenance and inspection records, and locating witnesses while memories are fresh.",
                "We then establish what the owner knew and when, which is what separates a claim that succeeds from one that does not. Georgia's shared-fault rule applies here too, and property owners routinely argue that the hazard was open and obvious, so documenting the actual conditions matters.",
            ]),
        ],
        "checklist": ("If you are hurt on someone's property", [
            "Report it to the owner or manager before leaving",
            "Ask that a written incident report be made, and request a copy",
            "Photograph the hazard immediately, from several angles",
            "Photograph the whole area, including lighting and signage",
            "Get names and contact details for any witnesses",
            "Keep the shoes and clothing you were wearing",
            "Seek medical attention even if the injury seems minor",
        ]),
        "faqs": [
            ("Do I have a claim if I did not notice the hazard?",
             "Possibly. Not noticing a hazard does not automatically defeat a claim, though property owners often argue that a danger was open and obvious. What matters is whether the owner met their duty of care and whether your own conduct was reasonable in the circumstances."),
            ("How quickly should I act?",
             "Quickly. Surveillance footage is frequently overwritten within days, and the hazard itself will usually be repaired or cleaned immediately. The legal deadline is longer than that, but the evidence that proves the claim often is not."),
            ("What if the store says it was my fault?",
             "That is a common response, and it is not the final word. Georgia reduces recovery by your share of fault and bars it entirely at 50 percent or more, so how fault is documented and argued directly affects the outcome."),
            ("Does this only apply to stores and businesses?",
             "No. Premises liability can apply to apartment complexes, parking areas, private residences, and public spaces. Who is responsible depends on who owned or controlled the area where the injury occurred."),
        ],
        "related": ["personal-injury", "dui-defense", "estate-planning"],
    },
    {
        "slug": "immigration",
        "num": "04",
        "nav": "Immigration Law",
        "title": "Atlanta Immigration Attorney | Family Visas & Green Cards | Jay Hutch Law",
        "description": "Jay Hutch Law guides clients through family-based immigration, adjustment of status, and visa matters — explaining options and preparing filings carefully. Free consultation.",
        "h1": "Immigration Law",
        "lede": "Immigration processes are federal, document-heavy, and unforgiving of errors. The goal is to understand your options clearly before filing anything.",
        "source": "practice_immigration",
        "sections": [
            ("Where the firm helps", [
                "We assist with family-based immigration petitions, adjustment of status, visa matters, and the supporting filings these processes require.",
                "Much of the work is understanding which path actually fits your situation. Eligibility depends on your relationship to a petitioner, your current status, how you entered the country, and your immigration history. Two people in apparently similar situations can have very different options.",
            ]),
            ("Why preparation matters more here than almost anywhere", [
                "Immigration filings are decided largely on the documents submitted. An incomplete petition can result in a request for evidence that adds months, or a denial that costs the filing fee and, in some cases, affects future applications.",
                "Processing times are long and they change. Priority dates move. Policies shift between administrations. Part of the work is setting realistic expectations about timing so you can plan around them rather than be surprised.",
                "Immigration law is federal, so these processes work the same way whether you are in Atlanta or anywhere else in the country. Where you live affects which office or court handles your matter, not the underlying law.",
            ]),
            ("How we work with clients", [
                "We begin by mapping your situation against the available paths, including the ones that will not work and why — that is often the most useful part of a first conversation.",
                "From there we identify what documentation will be needed, prepare the filings, and keep you informed as the matter moves. Where a matter falls outside what the firm handles, we will say so directly rather than take it on.",
            ]),
        ],
        "checklist": ("Helpful to bring to a consultation", [
            "Passports and any prior visas, for everyone involved",
            "Records of every entry into and exit from the United States",
            "Any notices or correspondence received from USCIS",
            "Marriage, birth, or adoption certificates where relevant",
            "Details of any prior applications, including denials",
            "Any criminal history, however minor or old",
        ]),
        "faqs": [
            ("How long do immigration cases take?",
             "It varies enormously by category and by the office handling the matter, and published processing times change. We will give you a realistic range for your specific path at the consultation rather than a general estimate that may not apply to you."),
            ("Can I file the paperwork myself?",
             "Many forms can be filed without an attorney. The risk is that eligibility questions are not always obvious from the forms themselves, and an error can cost far more in time than it saves. A consultation to confirm the right path is often worthwhile even if you handle the filing."),
            ("Does a criminal record affect my immigration case?",
             "It can, sometimes significantly, and sometimes for offences that seem minor or that were resolved years ago. Disclose anything in your history at the consultation so it can be assessed before anything is filed."),
            ("Do I need to be in Atlanta to work with the firm?",
             "Immigration law is federal, so the firm can assist regardless of where in the country you live. Contact the office to confirm."),
        ],
        "related": ["estate-planning", "personal-injury", "traffic-citations"],
    },
    {
        "slug": "estate-planning",
        "num": "05",
        "nav": "Estate Planning",
        "title": "Atlanta Estate Planning Attorney | Wills & Powers of Attorney | Jay Hutch Law",
        "description": "Wills, powers of attorney, and advance directives tailored to Georgia law. Jay Hutch Law helps families protect property and make their wishes clear. Free consultation.",
        "h1": "Estate Planning",
        "lede": "Estate planning is less about wealth than about clarity — making sure the people you trust can act, and that your wishes are known before anyone has to guess.",
        "source": "practice_estate",
        "sections": [
            ("What a plan usually includes", [
                "<strong>A will.</strong> Directs how your property is distributed and names an executor. It is also where parents of minor children name a guardian — often the single most important reason to have one.",
                "<strong>A financial power of attorney.</strong> Authorises someone to handle financial matters if you cannot. Without it, your family may need a court proceeding to do things as ordinary as paying your bills.",
                "<strong>An advance directive for health care.</strong> Georgia combines the living will and health care agent into one document, letting you name who decides for you and record your wishes about treatment.",
                "Depending on your circumstances, a plan may also involve trusts, beneficiary designations, or business succession arrangements.",
            ]),
            ("What happens without one", [
                "If you die without a will in Georgia, state intestacy law decides who inherits. The result is a fixed formula that may not reflect what you would have chosen — a surviving spouse shares with children rather than inheriting everything, and unmarried partners and stepchildren receive nothing.",
                "Without a power of attorney or advance directive, decisions that could have been made by someone you chose may instead require a court to appoint a guardian or conservator — a process that costs money, takes time, and happens at the worst possible moment.",
            ]),
            ("Practical points specific to Georgia", [
                "Georgia requires a will to be signed by the testator and witnessed by two competent witnesses. A self-proving affidavit, signed before a notary at the same time, can significantly simplify probate later.",
                "Georgia has no state estate tax, so for most families the planning question is not tax but clarity, access, and avoiding avoidable court involvement.",
                "A plan is not permanent. Marriage, divorce, a birth, a death, a move to another state, or a significant change in assets are all reasons to revisit documents you already have.",
            ]),
        ],
        "checklist": ("Worth thinking about beforehand", [
            "Who should manage your affairs if you cannot",
            "Who should raise your children, if that applies",
            "Who should receive what, and whether anyone needs protecting",
            "Where your accounts, policies, and deeds actually are",
            "Whether existing beneficiary designations still match your wishes",
            "Your wishes about medical treatment and who should speak for you",
        ]),
        "faqs": [
            ("Do I need an estate plan if I do not have significant assets?",
             "Most people benefit from at least a will, a financial power of attorney, and an advance directive. The powers of attorney and directive matter during your lifetime, and they matter regardless of how much you own. Naming a guardian for minor children has nothing to do with asset value at all."),
            ("What makes a will valid in Georgia?",
             "Georgia requires the will to be in writing, signed by the testator, and witnessed by two competent witnesses. Adding a self-proving affidavit at signing can make probate considerably simpler for the people you leave behind."),
            ("Is a will from another state still valid here?",
             "A will validly executed in another state is generally recognised in Georgia, but it is worth reviewing after a move. Terminology, procedure, and what makes probate straightforward differ from state to state."),
            ("How often should I update my plan?",
             "Review it after any significant life change — marriage, divorce, a birth, a death, a move, or a substantial change in assets — and otherwise every few years. Outdated beneficiary designations are one of the most common problems we see."),
        ],
        "related": ["immigration", "personal-injury", "premises-liability"],
    },
    {
        "slug": "traffic-citations",
        "num": "06",
        "nav": "Traffic Citations",
        "title": "Georgia Traffic Ticket Lawyer | Speeding & Super Speeder | Jay Hutch Law",
        "description": "Speeding, reckless driving, Super Speeder, and licence-related charges in Georgia. Jay Hutch Law works to protect your driving record and licence. Upload your citation for review.",
        "h1": "Traffic Citations",
        "lede": "Paying a ticket is a guilty plea. It is quick, and it is often the most expensive option once points, insurance, and licence consequences are counted.",
        "source": "practice_traffic",
        "urgent": "Paying a citation online is a conviction, not a settlement. Before you pay, it is worth understanding what it will add to your record. <a href=\"/upload-citation/\">Upload your citation</a> for a review.",
        "sections": [
            ("Why a ticket is rarely just a fine", [
                "Georgia assigns points to most moving violations, from two to six depending on the offence. Accumulating 15 points within any 24-month period results in licence suspension.",
                "Points also reach your insurance. A single speeding conviction can raise premiums for years, which routinely costs several times the fine itself. For drivers under 21, the thresholds are stricter — a single serious violation can mean suspension.",
                "If you hold a commercial licence, or your job depends on driving, the calculation changes again. Consequences that are inconvenient for most drivers can be disqualifying.",
            ]),
            ("Georgia's Super Speeder law", [
                "Georgia adds a Super Speeder fee for drivers convicted of travelling 75 mph or more on a two-lane road, or 85 mph or more on any road (O.C.G.A. § 40-6-189).",
                "The fee is separate from and additional to whatever the court imposes, and it is billed by the Department of Driver Services after the conviction. Failing to pay it within the required period results in licence suspension and a reinstatement fee on top.",
                "People are frequently caught out by this, because the court fine is paid and the matter seems closed until a suspension notice arrives.",
            ]),
            ("Charges the firm handles", [
                "Speeding and Super Speeder citations, reckless driving, aggressive driving, following too closely, failure to yield, improper lane change, driving without a valid licence or insurance, and suspended licence charges.",
                "Some of these are misdemeanours rather than simple traffic infractions — reckless driving among them — which means a criminal record, not just points.",
            ]),
            ("What we do", [
                "We review the citation and the circumstances, explain what a conviction would actually cost you across points, insurance, and licence status, and identify whether an alternative resolution is available.",
                "For many citations we can appear on your behalf, so you do not have to take a day off work to attend court. Whether that applies depends on the charge and the court.",
            ]),
        ],
        "checklist": ("Before you pay that ticket", [
            "Check the response deadline printed on the citation",
            "Note the exact charge and the recorded speed",
            "Check whether the court date requires you to appear",
            "Count the points you already have from the past 24 months",
            "Consider what a conviction does to your insurance",
            "Get it reviewed before the deadline, not after",
        ]),
        "faqs": [
            ("Can I just pay the ticket online?",
             "You can, but paying is pleading guilty. The conviction goes on your record with its points, reaches your insurer, and cannot be undone afterwards. It is worth understanding the full cost before choosing that route."),
            ("How many points suspend a licence in Georgia?",
             "Fifteen points within a 24-month period results in suspension for most drivers. Individual violations carry two to six points. Drivers under 21 face stricter rules, where a single serious violation can trigger suspension."),
            ("What is a Super Speeder fee?",
             "Georgia charges an additional state fee for convictions involving speeds of 75 mph or more on a two-lane road, or 85 mph or more on any road. It is billed separately by the Department of Driver Services after conviction, and not paying it leads to suspension."),
            ("Do I have to appear in court?",
             "It depends on the charge and the court. For many citations the firm can appear on your behalf. Until that is confirmed, do not miss any date listed on your citation."),
        ],
        "related": ["dui-defense", "personal-injury", "premises-liability"],
    },
]

BY_SLUG = {p["slug"]: p for p in PAGES}

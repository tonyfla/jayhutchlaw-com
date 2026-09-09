# -*- coding: utf-8 -*-
"""Content source for /resources/.

STATUS: DRAFT. Same review requirement as the practice-area pages — these are
published under the firm's name and need J. Hutchins to read them first.

Design note: the guide text is always open and indexable. Gating an article
removes it from search results, which defeats the point of writing it. The
gate (when enabled) applies to the downloadable companion, not the reading.
"""

HUB = {
    "title": "Legal Guides & Resources | Georgia | Jay Hutch Law",
    "description": "Plain-language guides to Georgia legal matters from Jay Hutch Law — what to do after a car accident, the first 48 hours after a DUI arrest, and what a traffic conviction actually costs.",
    "h1": "Guides worth reading before you need them.",
    "lede": "Practical, plain-language explanations of the Georgia legal situations people most often find themselves in unexpectedly. Free to read, no form required.",
}

GUIDES = [
    {
        "slug": "after-a-car-accident-in-georgia",
        "nav": "After a Car Accident in Georgia",
        "kicker": "Personal injury",
        "read_time": "8 min read",
        "title": "What to Do After a Car Accident in Georgia | Jay Hutch Law",
        "description": "A step-by-step guide to the hours, days, and weeks after a Georgia car accident — what to document, what not to say, and the deadlines that matter.",
        "h1": "What to do after a car accident in Georgia",
        "lede": "The decisions made in the first few days after a collision shape what is possible months later. This is what matters, in order.",
        "related_practice": ("personal-injury", "Personal Injury"),
        "source": "guide_car_accident",
        "sections": [
            ("At the scene", [
                "Check for injuries and call 911. In Georgia you are required to report an accident involving injury, death, or apparent property damage of $500 or more — a threshold almost any modern collision clears. A police report also creates an independent record, which matters later.",
                "Move vehicles out of traffic if they are drivable and it is safe. Otherwise leave them and get yourself to safety.",
                "Exchange names, contact details, insurance information, and licence plate numbers. You do not need to discuss what happened to do this.",
                "<strong>Photograph more than you think you need.</strong> All vehicles from several angles, the position of the vehicles before they are moved, skid marks, debris, traffic signals and signs, road conditions, the weather, and any visible injuries. These images cannot be recreated later.",
                "Get names and phone numbers for any witnesses. Witnesses disappear, and the police report may not include everyone.",
            ]),
            ("What not to say", [
                "Do not apologise or accept blame, even reflexively. Georgia reduces your compensation by your share of fault and bars recovery entirely at 50 percent or more, so a casual \"I'm so sorry\" at the roadside can be quoted back at you.",
                "Do not say you are uninjured. Adrenaline masks injury, and soft-tissue and head injuries frequently take a day or more to present. \"I don't know yet\" is both true and safer.",
                "Do not give a recorded statement to the other driver's insurer. They are entitled to ask; you are not obliged to agree, and it is worth speaking to an attorney first.",
            ]),
            ("In the first 72 hours", [
                "<strong>Get examined, even if you feel fine.</strong> This matters medically, and it also creates a dated record connecting the collision to your injuries. A gap between the accident and your first medical visit is the most common argument insurers use to reduce a claim.",
                "Report the accident to your own insurer, factually, without speculating about fault.",
                "Start a file: the police report number, medical records, receipts, and a note of every missed day of work.",
                "Keep a short daily note of pain, limitations, and what you could not do. Reconstructing this months later is nearly impossible and much less credible.",
            ]),
            ("The deadlines that end claims", [
                "<strong>Two years.</strong> Georgia generally allows two years from the date of injury to file a personal injury lawsuit (O.C.G.A. § 9-3-33). Property damage claims generally allow four years.",
                "<strong>Much less, against a government entity.</strong> If a city, county, or state vehicle or road condition was involved, ante litem notice requirements apply and they are measured in months, not years. These are missed routinely.",
                "<strong>Your own policy's deadline.</strong> Uninsured and underinsured motorist coverage carries its own notice requirements, set by the policy rather than by statute.",
            ]),
            ("About that first offer", [
                "Early settlement offers usually arrive before anyone knows the full extent of an injury — often before treatment has finished. Accepting one generally closes the claim permanently, including for costs that have not yet appeared.",
                "There is no obligation to accept, and no obligation to respond quickly. The pressure to settle fast is not a legal requirement; it is a negotiating position.",
            ]),
        ],
        "takeaway": [
            "Call 911 and get a police report",
            "Photograph everything before vehicles are moved",
            "Do not apologise, and do not say you are uninjured",
            "See a doctor within 72 hours even if you feel fine",
            "Decline a recorded statement until you have advice",
            "Note the two-year deadline — and much shorter ones if a government vehicle was involved",
        ],
        "faqs": [
            ("Do I have to report a minor accident in Georgia?",
             "Georgia requires reporting where there is injury, death, or apparent property damage of $500 or more. Most collisions meet that threshold, and a report is useful evidence even when it is not strictly required."),
            ("The other driver wants to settle without insurance. Should I?",
             "Be cautious. Damage and injuries are frequently worse than they appear at the roadside, and once you have agreed and separated, you may have no practical way to recover more. At minimum, document everything and get a medical assessment first."),
            ("How long do I have to file a claim?",
             "Generally two years from the date of injury in Georgia for personal injury, and four years for property damage. Claims involving a government entity carry far shorter notice requirements, sometimes only a few months."),
        ],
    },
    {
        "slug": "first-48-hours-after-a-georgia-dui-arrest",
        "nav": "The First 48 Hours After a DUI Arrest",
        "kicker": "DUI defense",
        "read_time": "7 min read",
        "title": "The First 48 Hours After a Georgia DUI Arrest | Jay Hutch Law",
        "description": "A Georgia DUI arrest starts a licence clock separate from your court case, and it runs in days. Here is what to do first, and the mistake that costs people their licence.",
        "h1": "The first 48 hours after a Georgia DUI arrest",
        "lede": "There are two cases, not one — and the one nobody tells you about moves first.",
        "related_practice": ("dui-defense", "DUI Defense"),
        "source": "guide_dui_48h",
        "urgent": "If you have been arrested for DUI in Georgia, the deadline affecting your driver's licence has already started running. Call <a href=\"tel:+18554882452\">855-488-2452</a> before reading further if you are close to it.",
        "sections": [
            ("The mistake almost everyone makes", [
                "A Georgia DUI arrest creates two entirely separate proceedings. Most people know about one of them.",
                "<strong>The criminal case</strong> is what happens in court. It has a date, you were given paperwork about it, and it will take months.",
                "<strong>The administrative case</strong> is an action against your driver's licence, handled by the Department of Driver Services. It is not the same case, it is not decided by the same people, and it moves first. The window to contest it begins on the date of arrest and is measured in days.",
                "People assume the court date is the thing to prepare for, let the licence deadline pass unnoticed, and lose driving privileges before they have ever seen a judge. This is the single most consequential and most avoidable error after a DUI arrest.",
            ]),
            ("What to do immediately", [
                "<strong>Write down the date of arrest.</strong> Everything is measured from it.",
                "<strong>Find every piece of paper you were given.</strong> The citation, any notice about your licence, the bond paperwork. Do not throw away anything, including what looks like a receipt.",
                "<strong>Write down what you remember, now.</strong> Where you were coming from, what you had eaten and when, what the officer said, what tests you were asked to perform and in what conditions, whether you were read anything and at what point. Memory for this degrades within days.",
                "<strong>Note any medical conditions</strong> that affect balance, coordination, speech, or breath testing — inner ear problems, injuries, diabetes, acid reflux, and others can all matter.",
            ]),
            ("What not to do", [
                "Do not post about it. Social media content is discoverable and is routinely used.",
                "Do not discuss the arrest with anyone other than an attorney. Conversations with friends and family are not privileged and those people can be asked about them.",
                "Do not miss the court date, whatever else is happening. A failure to appear creates a separate and more serious problem on top of the DUI.",
                "Do not assume the case is hopeless because you think you failed a test. How a test was administered, whether equipment was maintained, and whether procedure was followed are all reviewable, and none of it is visible from the roadside.",
            ]),
            ("What gets examined", [
                "<strong>The stop.</strong> An officer needs a lawful basis to pull a vehicle over. If it does not hold, what followed may be challenged.",
                "<strong>Field sobriety testing.</strong> These are standardised tests that only mean anything when administered as designed — on level ground, with correct instructions, accounting for footwear, injuries, and conditions.",
                "<strong>Chemical testing.</strong> Breath and blood testing depend on maintained equipment, correct procedure, and an intact chain of custody. Georgia's implied consent notice must also be read correctly and at the right moment.",
                "<strong>Refusal.</strong> If you declined testing, that carries its own licence consequences under implied consent — and its own set of questions about whether the notice was properly given.",
            ]),
        ],
        "takeaway": [
            "Note your exact arrest date — the licence clock starts there",
            "Keep every document you were given",
            "Write down what you remember today, not next week",
            "Say nothing about it publicly or to friends",
            "Do not miss your court date",
            "Speak to an attorney before the licence deadline, not after",
        ],
        "faqs": [
            ("What is the licence deadline after a Georgia DUI arrest?",
             "The administrative action against your licence has a short deadline that begins on the date of arrest and is measured in days rather than weeks. Because the exact requirement depends on the circumstances of your arrest, confirm it with an attorney immediately rather than relying on a general figure."),
            ("Is refusing the breath test better?",
             "Not automatically. Refusal carries its own licence consequences under Georgia's implied consent law and can be raised in the case. Whether it helps or hurts is entirely fact-specific."),
            ("Can a DUI be removed from my record later?",
             "A Georgia DUI conviction generally remains on the record and is not eligible for restriction the way some other offences are. That is a large part of why how the case is handled at the start matters so much."),
        ],
    },
    {
        "slug": "what-a-georgia-traffic-ticket-really-costs",
        "nav": "What a Georgia Traffic Ticket Really Costs",
        "kicker": "Traffic citations",
        "read_time": "6 min read",
        "title": "What a Georgia Traffic Ticket Really Costs | Points & Super Speeder",
        "description": "The fine is the smallest part. A guide to Georgia's points system, the Super Speeder fee, insurance consequences, and why paying online is a guilty plea.",
        "h1": "What a Georgia traffic ticket really costs",
        "lede": "The number printed on the citation is usually the smallest figure involved. Here is the rest of it.",
        "related_practice": ("traffic-citations", "Traffic Citations"),
        "source": "guide_ticket_cost",
        "urgent": "Paying a citation online is a guilty plea. It is entered as a conviction, it cannot be undone afterwards, and it is often the most expensive option available. <a href=\"/upload-citation/\">Upload your citation</a> before you pay.",
        "sections": [
            ("Paying is pleading guilty", [
                "The online payment portal makes a citation feel like a bill. It is not. Paying enters a conviction against you, with everything that follows from it — and once entered, it generally cannot be reopened.",
                "This is why the convenient option is so often the costly one. The fine ends; the conviction does not.",
            ]),
            ("Points, and the number that suspends a licence", [
                "Georgia assigns points to moving violations, generally between two and six depending on the offence. <strong>Accumulating 15 points within any 24-month period results in licence suspension.</strong>",
                "Points are cumulative across citations, which is why a driver with a clean record and a driver with two prior tickets face very different situations over the same charge.",
                "Drivers under 21 face stricter rules, where a single serious violation can result in suspension without approaching 15 points.",
            ]),
            ("The Super Speeder fee people do not see coming", [
                "Georgia adds a Super Speeder fee for convictions involving speeds of <strong>75 mph or more on a two-lane road, or 85 mph or more on any road</strong> (O.C.G.A. § 40-6-189).",
                "It is separate from and additional to whatever the court imposes, and it is billed afterwards by the Department of Driver Services. People pay the court fine, consider the matter closed, and then receive a notice they were not expecting.",
                "Failing to pay it within the required period results in licence suspension plus a reinstatement fee on top of the original amount.",
            ]),
            ("The insurance cost, which is usually the largest", [
                "A single speeding conviction commonly affects premiums for around three years. Across that period the increase frequently exceeds the fine several times over, which means the true cost of a citation is usually measured in the hundreds or thousands rather than the amount printed on it.",
                "This is the figure worth calculating before deciding how to handle a ticket, and it is the one most people never calculate at all.",
            ]),
            ("When a ticket is not just a ticket", [
                "Some charges commonly written as traffic citations are misdemeanours, not infractions — reckless driving among them. A conviction is a criminal record, not merely points.",
                "If you hold a commercial licence, the rules are stricter and the consequences reach your livelihood directly. The same is true if your job requires driving or a clean record.",
            ]),
        ],
        "takeaway": [
            "Paying online is a guilty plea, not a settlement",
            "15 points in 24 months suspends a Georgia licence",
            "Super Speeder adds a separate fee billed after conviction",
            "Insurance is usually the largest cost, over about three years",
            "Reckless driving is a misdemeanour, not an infraction",
            "Check the response deadline before doing anything else",
        ],
        "faqs": [
            ("Is it cheaper to just pay the ticket?",
             "Rarely, once insurance is counted. The fine is a one-time cost; a conviction affects premiums for roughly three years and adds points that may combine with future citations. The convenient option is usually the expensive one."),
            ("How many points is a speeding ticket in Georgia?",
             "It depends on how far over the limit the recorded speed was, generally ranging from two to six points. Speeds of 15 mph or less over the limit carry fewer points than higher ranges."),
            ("What happens if I ignore a citation?",
             "Failing to respond by the deadline can result in a failure-to-appear, licence suspension, and in some cases a bench warrant. Ignoring a citation always makes the situation worse than the original charge."),
        ],
    },
]

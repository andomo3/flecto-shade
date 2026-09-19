# Judge Q&A bank

The playbook's fifteen questions, turned toward this project, then the ones only this project will get.
Every answer follows the playbook's formula: the direct answer in ten seconds, the evidence in twenty, the honest scope in ten.
Never bluff a capability: nothing here is physical, nothing here is measured, and the answer to an expert's objection opens by conceding it.

Who answers: Ameya takes the data and the simulation, Shannon takes the roof layout and what the fin's publications say, and abba takes the page, the rules, and the figures.
Anything in square brackets is filled in at the event, from what was actually built.
Every simulation figure is provisional, from the planner's run in `../plans/packages/H1-zones-light-rain-soil.md`, and is confirmed against `data/processed/headline.json` before it is said.

## The fifteen

**1. Who is this for, specifically?**
"A grower with several crops under one shade house roof.
We set it near Apopka, in Central Florida, because the University of Florida's centre there calls it the heart of Florida's greenhouse and nursery industry, and shade houses are the practice there.
Elena, in our pitch, is an illustration.
We have not spoken to a grower."

**2. What problem does it solve that existing roofs do not?**
"Resolution, and only that.
A UMass fact sheet says one gear motor handles up to fifty thousand square feet of retractable roof, and one screen motor up to forty thousand.
So every plant under it gets one decision.
A roof of many small fins can treat one bed differently from the next.
Everything else, the light targets and the watering logic, already exists, and we say so."

**3. How did you validate that anyone wants this?**
"We did not, and I will not pretend we did.
Our evidence that the problem is real is published: Purdue's light table puts Boston fern at its best from eight mol a day and hydrangea from twelve, under roofs that make one decision.
Whether a grower would pay for the difference is unknown."

**4. What did you build, and what is mocked?**
"Built this weekend: the simulation, the page, the result card, and the gate runner that checks them.
Nothing physical was built.
Real inputs: one year of hourly rain from the Orlando Executive Airport gauge, and the sun for the same place and year from NASA POWER, which is a satellite product and so is modelled.
Everything the page shows is simulated, and the page says so on every figure."

**5. What breaks if this were scaled up?**
"Everything we did not model: wind, hail, the fatigue of a fin over years, the count of actuators, and disease from wet leaves.
The card on the table lists them.
We make no claim about any of them."

**6. How does the smart part work? Is there AI in it?**
"No AI and no learned model, on purpose.
Nine written rules, in the priority night, then rain, then light, and two runs give identical bytes.
The fins never follow the sun's position: they react to how much light has arrived, to rain, and to the soil.
The logic itself is standard practice in greenhouse computers.
AI tools wrote code from our specifications, and they are cited in the submission."

**7. What happens when the network or the data is unavailable?**
"Nothing changes.
It builds and runs with no network, the two data files are on the disk, and the page fetches nothing from the internet.
If the page fails, there is a recorded run of the same day, and behind that a screen recording."

**8. Where does the data come from, and who can see it?**
"The rain is NOAA's global hourly record for the Orlando Executive Airport gauge, 2023.
The sun and the temperature are NASA POWER for the same point and year.
The crop figures are from Purdue, Washington State, and the FAO's irrigation paper 56, each cited with its address.
There is no personal data anywhere."

**9. Why this stack?**
"Python with pandas for the simulation, and one plain page of HTML, CSS, and JavaScript.
No framework, no build step, and no network, so nothing could break at 3 am at a crowded venue, and every spoken figure comes from one file the build writes."

**10. What would you cut with four fewer hours?**
"[Filled in at the event.
The plan's order: the second view that draws the fins one by one, then the year view, and the one day playing end to end was always safe.]"

**11. What would you build with four more weeks?**
"Three things.
A conversation with a grower near Apopka about where this is wrong.
A soil bucket sized for containers, because nursery stock is often grown in them and ours is an assumed sixty millimetres.
And wind, which the simulation does not model."

**12. How would this reach a real grower?**
"Through a conversation, not a sale: one grower, or the University of Florida's research centre in Apopka, shown the rules and asked what is wrong with them.
After that, a small row of fins on one actuator.
We have done neither."

**13. What did each of you own?**
"Ameya the data and the simulation, Shannon the roof layout, and abba the page, the result card, the integration, and this pitch.
Each of us drove a build agent in the same repo, so the seams between us were files with written schemas."

**14. What was the hardest problem, and how did you solve it?**
"[Filled in at the event, by whoever fought it.
One candidate, from the planning: a typical solar year joined to a real year of rain made rainy hours brighter than dry ones, so we took the sun from the same place and year as the rain, and now rainy daylight hours carry about 0.63 of the light of dry ones, modelled.]"

**15. Can I try it myself right now?**
"Please.
Press Play."

## The ones only this project gets

**Growers keep rain off crops, so why let it in?**
"You are right, and we concede it for a glasshouse, for ferns, and for fruit near harvest.
Cravo, who make roofs that open, close them before the rain.
That is why this is a shade house, why each crop opts in, only in daylight, only with time to dry, and why the fern opts out.
We claim the water arithmetic and never safety from disease."

**Your logic is already in Priva.**
"Yes.
Ridder and Hoogendoorn water by the radiation sum, Argus sells a daily light integral program, and Priva steers screens from a light sensor.
The contribution is the resolution of the actuator, a bed and not a bay, and not the algorithm."

**Is this real?**
"No.
The rain is a real gauge, the sun is a satellite product for the same hours, the soil and crop numbers are textbook coefficients with assumed bucket sizes, and nothing physical was built."

**Why is there no physical prototype?**
"Because the fin is not where our work is.
It is an existing mechanism, published and patented by its inventors, so printing one would have shown their idea and not ours.
Our contribution is the zone by zone control and the simulation over a real year of weather, and the hours went there.
We claim nothing about the fin's mechanics."

**Is the fin your idea?**
"No.
It is the Flectofin, by ITKE at the University of Stuttgart with the University of Freiburg, patented as EP2320015, and the page credits it.
We found no prior proposal to put a Flectofin over crops, and that is an absence in our searches, not proof."

**What about wind and hail on thin fins?**
"Unproven.
The simulation does not model wind, and closing and stowing in a storm is future work."

**What does it cost against a screen at two dollars a square foot?**
"We make no cost claim.
One actuator a row would keep the actuator count near that of screens, and that is a hypothesis, not a finding."

**Why would a hingeless fin matter here?**
"The sources document the chores it removes: an insurer's guide tells growers to lubricate bearings, racks, and vent hinge points, and a university fact sheet asks for cable tension kept and gear motors lubricated once or twice a year.
A fin with no hinge removes documented maintenance tasks.
No saving is quantified, by them or by us."

**Why Apopka, and why is your gauge in Orlando?**
"Apopka because of the industry there, in the University of Florida's own words.
Orlando Executive Airport because, of four gauges near Apopka, it was the most complete: 8,760 hourly reports with two lacking the rain field.
The page names the gauge and says near Apopka."

**Was 2023 a special year?**
"No.
At that gauge it was 2.4 percent above the 1991 to 2020 normal for rain, an ordinary year.
It is still one year."

**The rain supplied 54 percent of the hydrangea's water. Is that water saved?**
"No, and we never say so.
It is the rain the zone's soil stored, over that rain plus the grower's irrigation, in a simulated year with an assumed soil bucket.
For the blueberry zone it is about 17 percent, and for the fern it is zero, because the fern opted out."

**Opening for the rain gave the hydrangea light it did not want. Why not fix that?**
"Because it is the honest price of the rule, and it is on the card: about six mol on the demo day.
The priority is night, then rain, then light, and a fin that lets rain through lets light through."

**How sure are you of the demo day?**
"We scaled the evaporation from 0.95 to 1.05 in seven runs.
The blueberry's answer held in all seven, and the hydrangea's in six, and the fern opts out whatever its soil does.
The blueberry stays shut on a margin of 1.2 millimetres of soil water, and the rain hour at three sits 1.1 millimetres under the hard rain cap.
Those are the gauge's readings and nothing was tuned, and we say how thin they are."

**Your sun is a satellite cell. Does it see the storm?**
"Not always.
The cell is about 100 kilometres across, so a local storm can rain under a bright cell, as on 29 July 2023.
On the demo day the sun dims as the rain arrives and does not collapse.
The page says the sun is modelled."

**Are your light sums right?**
"They may read 5 to 18 percent high.
We convert global solar to plant light with 0.45, a choice inside the published range, and field values sit lower.
It is a named constant and a row in the README's table of assumptions."

**Why shade blueberries in Florida?**
"It is not Florida practice, and the page says so.
The 30 to 50 percent figure is a heat recommendation from Washington State University.
The blueberry zone is the weakest of the three."

**How many fins, and how many motors?**
"[From Shannon's roof layout, as a modelled design.]
The simulation treats a zone's roof as one open fraction, so the layout changes what you see and never a figure on the card.
We claim nothing about actuators."

**An open roof loses heat, and carbon dioxide where it is dosed.**
"Agreed, which is another reason this is an unheated shade house and not a glasshouse."

**What did you build this weekend, and what did you plan before?**
"Everything in the repo was written during the event.
The planning repo is public and linked, and it shows the project changed direction four times on Saturday: a bus shelter roof, a simulated one, a leaf design tool, and this.
That is true, and the commit history shows it."

**How did three of you use the build agents?**
"One package, one branch, one owner.
Every expected value was computed from the real data before any code existed, so an agent could not pass by agreeing with its own mistake, and gates ran after every package.
It is all in `CHECKLIST.md`."

## Rules for the table

- Thirty seconds an answer, then stop.
- Answer the question asked, and let the person who built the thing answer it.
- To an expert, concede before explaining.
- "We did not get to that, and here is how I would find out" is always allowed, and bluffing never is.
- End with "thank you", never with "that's all".

## Where each figure came from

| Figure | File |
|---|---|
| 50,000 and 40,000 square feet a motor, the makers and what each sells, the maintenance chores, the two dollars in the judge's question | `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md` |
| 8 and 12 mol, 30 to 50 percent, the four gauges and 8,760 reports, 2.4 percent, 0.63, 54 and 17 percent, 6 mol, the seven runs, 1.2 and 1.1 mm, 5 to 18 percent, the 60 mm bucket | `../plans/packages/H1-zones-light-rain-soil.md`, the simulation figures provisional until `headline.json` exists |
| The 100 km cell and 29 July 2023 | `../plans/plan-d-louvre-roof.md` and `../plans/packages/S1-solar-2023.md` |
| The patent and the two universities | `../docs/research/flectofin-design-tool/sector-choice.md` |

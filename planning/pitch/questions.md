# Judge Q&A bank

The playbook's fifteen questions, turned toward this project, then the ones only this project will get.
Every answer follows the playbook's formula: the direct answer in ten seconds, the evidence in twenty, the honest scope in ten.
Never bluff a live capability: offer the recording instead.

Who answers: the engineers take the leaf, the mechanism, and the electronics, and abba takes the data, the app, and the numbers.
Anything in square brackets is filled in at the event, from what was actually built and measured.

## The fifteen

**1. Who is this for, specifically?**
"A rider waiting at an unshaded bus stop in a hot city. We picked Houston because researchers measured seventeen stops there in the summer of 2023, and because only about one in six Houston stops has a shelter at all. The buyer would be a transit agency, and we have not spoken to one yet."

**2. What problem does it solve that existing shelters do not?**
"Two things. In that Houston study the worst shelter was five degrees hotter than standing in the open, because its closed walls trapped the heat. And a fixed roof is built for one sun angle, which the sun holds for about an hour. Ours opens to the air and changes shape with the light. What we have shown is the light on the bench, on a model, and nothing about a full size shelter."

**3. How did you validate that anyone wants this?**
"We did not interview riders, and I will not pretend we did. Our evidence that the problem is real is the published study and the city's own shelter count. Rosa, in our pitch, is an illustration and we say so."

**4. What did you build, and what is mocked?**
"Built this weekend: the leaves, the rig, the firmware, the app, and the data pipeline. Real: the sensor readings and the leaf motion you just watched. Simulated: the sun is an LED following a real day's solar data, and [the sun's position is fixed / the sun moves on a servo]. Nothing on that screen is a recorded number unless the banner says recorded run."

**5. What breaks if this were scaled up?**
"Everything we did not test: wind, rain, fatigue over thousands of cycles, vandalism, and cost. The card on the table lists them. The one thing in our favour is that a hingeless leaf has no joint to seize, which is why the researchers who developed the principle proposed it for shading building facades."

If the judge presses on rain: "Sensing rain and reacting to it is solved: louvred pergolas already close on a rain sensor, and our leaves already move on one sensor. What is not proven is whether the closed leaves shed water, and that is the first full size test. If they do not, a clear sheet under the leaves handles the rain and the leaves handle the sun. And where the summer is nearly rainless, like the fields of California's Central Valley, the same leaf shades a farmworker's break with nothing else needed."

**6. How does the smart part work? Is there AI in it?**
"No AI, on purpose. It is a light sensor and a threshold with a little hysteresis so it does not flutter. A bus shelter should be as dumb and reliable as a thermostat. The intelligence is in the shape of the leaf."

**7. What happens when the laptop or the data is unavailable?**
"The canopy does not need either. Unplug the laptop and the leaves still follow the light, because the control runs on the board. The laptop only plays the sun and draws the screen, and the dataset is a file on the disk, downloaded before the event."

**8. Where does the data come from, and who can see it?**
"The solar data is the European Commission's PVGIS typical year for Houston, open and free, and the sun's position is computed with the open source pvlib library. There is no personal data anywhere: the only things we record are light readings from our own table."

**9. Why this stack?**
"An Arduino, because a threshold does not need more. Python and one static page, because it had to run with no network at a crowded venue. No framework, no build step, so nothing could break at 3 am."

**10. What would you cut with four fewer hours?**
"[The servo mounted sun and the temperature sensors], in that order. We wrote the pivots down before the event with the hour each one fires, so the core loop was always safe: light, leaves, number."

**11. What would you build with four more weeks?**
"Three things. A full size leaf in a weatherproof material. A week of outdoor measurement with a real heat stress instrument rather than a light sensor. And a conversation with one transit agency about one real stop."

**12. How would this reach its first real stop?**
"Through a pilot, not a sale: one agency, one stop, one summer, with the measurement published either way. Houston already maps which stops have shelters, so the first candidates are easy to find."

**13. What did each of you own?**
"[Engineer one] the leaves and the mechanism, [engineer two] the rig and the electronics, and I did the firmware, the app, the data, and this pitch. We are three people, so the seams between us were written down before we started."

**14. What was the hardest problem, and how did you solve it?**
"[Filled in at the event, by whoever fought it. Most likely getting three leaves to buckle the same way from one motor.]"

**15. Can I try it myself right now?**
"Please. Press play, and then put your hand over that sensor."

## The ones only this project gets

**How does it know where the sun is?**
"It does not, and it does not need to. It reacts to the light that actually arrives, so a cloud, a tree, or a parked truck are all handled the same way."

**Is the app just playing a script?**
"The app plays the sun. Nothing plays the leaves. Cover the sensor and they relax, uncover it and they bend, whatever the app is doing."
If replay mode is on: "Right now, yes: this room's lighting fools our sensor, so the app is driving the leaves from the data and the banner says so. Here is this morning's recording of the sensor doing it."

**Why not just build a bigger fixed roof?**
"A bigger roof is more material, more wind load, and it blocks the winter sun riders want. This one shades at midday and opens when the light is gentle. [If the backup fixed roof was built: and here is the fixed roof beside it, reading Z percent.]"

**If bent is the shading state, why not leave it bent all summer? What does moving buy?**
"At noon in July, nothing: a closed fixed roof shades just as well, and we will not pretend otherwise. Moving buys the other hours. Open, the roof lets air through, and the shelter that was hotter than the open in the Houston study failed because it was closed in and trapped heat. Open, it lets the low winter sun in, keeps the stop visible at night, and turns its blades edge on to a storm. [If the backup fixed roof was built: and here is the fixed roof beside it.] What we measured is only the two states, bent and resting."

**The study says that shelter was hot because it trapped heat, not because the sun moved. Does your roof fix that?**
"You are right about the study, and we say it that way. Its cause was closed acrylic and metal walls. Our answer to that is the resting state: open blades with sky between them, nothing closed in. The moving sun is our second argument, not the study's. We have not measured temperature under either state."

**The same study found trees were the best shade. Why not plant a tree?**
"Plant the tree. It was the best thing they measured, almost six degrees. But a tree takes years to cast a bench's worth of shade, needs soil and water, and many stops are a pole in a strip of concrete. This is for the stop where a tree cannot go, and for the years before the tree grows."

**Houston METRO is already putting in ventilated shelters with perforated walls. Why is this needed?**
"That is the same lesson we took from the study, and it fixes the trapped heat. It does not fix the shade drifting off the bench as the sun moves, because the roof is still fixed. [Verify the METRO programme at a METRO source before saying any number about it.]"

**Only one in six stops has any shelter, because shelters cost money. Why would an agency buy a dearer one?**
"They would not, for every stop. It belongs at the few stops where the most riders wait the longest in the harshest sun, [and our data analysis ranks exactly those stops, if it ships]. We have no cost number for a full size leaf."

**Where does the power come from at a stop with no mains?**
"[Engineers to confirm.] The leaves move about twice a day and hold their shape in between, so the energy is small: the intended answer is a small panel and a battery, the way lit shelters already work. We ran ours from [the bench supply], and we did not measure the energy per cycle."

**What happens when the motor or the sensor fails?**
"[Engineers to confirm which state the leaf returns to with no power.] It should fail to whichever state is safer in a storm, which is resting and edge on. A failed leaf is then an open pergola, not a hazard."

**Your sun is an LED a few centimetres away. Does the [X] against [Y] carry over to the real sun?**
"The direction does, and the size does not. An LED that close is a point of light, the real sun's rays are parallel, and the sky adds diffuse light from every side. That is why the card says under an LED sun. The real number needs a real afternoon outdoors."

**How sure are you of those two numbers?**
"[N] readings in each state across [N] cycles, mean [X] with a spread of [S], mean [Y] with a spread of [S]. The two ranges [do / do not] overlap. One table, one room, one day."

**What about the late afternoon, when the sun is low and comes in under any roof?**
"An overhead leaf does nothing for a low sun, and that is true of every roof. In our geometric model a leaf on the sunward eave added far more shade hours than a roof tilting about its centre. That is modelled with placeholder dimensions, not measured."

**You measured light. Is that the same as heat?**
"No, and we do not claim it is. Direct sun is a large part of what a rider feels at a bus stop, and light is what we could measure honestly in a day on a table under an LED. Temperature needs a real sun and a real afternoon. [If the temperature sensors read: we logged temperature as well, and it showed D degrees, which we treat as a footnote.]"

**What is the leaf made of, and how long does it last?**
"[Material and thickness, from the engineers.] It survived [N] cycles this weekend. Fatigue life is a real question and we have not answered it."

**What does it cost?**
"The model is [one hobby servo, a few sensors, and printed parts]. We have no honest number for a full size one."

**Is this your idea?**
"The bending principle is called Flectofin, developed by researchers at the University of Stuttgart from the bird of paradise flower, as a shading system for building facades. Putting it on a bus stop, driving it from a light threshold, and measuring the bench is ours. [Confirm with the engineers that Flectofin is the mechanism before saying this.]"

**What did you do before the event?**
"Research, planning, and one throwaway prototype of the serial format to check our spec, all public: the planning repo is linked from our README and the prototype is labelled there. None of it was copied. Every line of code and every part in front of you was made after eleven on Saturday."

**Why does it matter beyond Houston?**
"Every hot city has riders and stops. The same leaf works over a farmworker's rest shade or a grower's crop, and that card shows three. [If the city picker shipped: and here is the same day in another city.]"

## Rules for the table

- Thirty seconds an answer, then stop.
- Answer the question asked, and let the person who built the thing answer it.
- "We did not get to that, and here is how I would find out" is always allowed, and bluffing never is.
- End with "thank you", never with "that's all".

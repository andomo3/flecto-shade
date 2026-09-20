# The 90 second video script

Written on 2026-09-20 through the `hackathon-pitch` skill, as a cut of `story.md`.
It is written against the page as it is on `main` at commit `752dbe4`, which the planner ran in a browser before writing a word.
It replaces the line in `video.md` that says the submission video uses the 60 second script.

Every figure spoken here is in `software/page/day.json` and is shown on the page, or is a sourced figure from `story.md`.
No figure for the year is spoken, because `headline.json` does not exist yet.
Elena is an illustrative name, introduced with "picture", because nobody was interviewed.
The closing line is a working draft, and abba replaces it in abba's own voice.

## The voiceover

Count: 233 words, inside the 225 to 270 that 90 seconds allows at the playbook's pace, and at the low end on purpose, because the screen talks twice.
Counted as whitespace separated words in the spoken text only, and counted again after any edit.

### 0:00 to 0:21, the problem, over the roof before the run

"Picture Elena, a foliage grower near Apopka, Florida.
The University of Florida's table lists fifty crops, with shade from thirty percent to ninety.
But her shade is one curtain on one motor, and one motor can cover most of a football field.
So every bed gets the same.
So to change a plant's light, Elena moves the plant."

### 0:21 to 0:36, the turn and the credit, over the module view

"What if the roof moved instead, bed by bed?
That takes many small parts, so we borrowed one with no hinge: the Flectofin, by ITKE in Stuttgart.
The fin is theirs, the logic is standard, and all of it is simulated."

### 0:36 to 0:50, the day, over the run

"The third of June, 2023: a real rain gauge, and a modelled sun.
By eleven the fern has its light, and its roof shuts.
By noon, the hydrangea.
The blueberries want all of it, and stay open."

### 0:50 to 1:08, the storm, over the run and then the held frame

"Then the storm: forty two millimetres in two hours.
One storm, three answers.
The hydrangea's soil is dry, so its roof opens for the rain.
The blueberries' soil is wet enough, so the rain is kept off.
And the fern never takes rain: its foliage stays dry."

### 1:08 to 1:22, the limits and what comes next, over the decision log

"Nothing was built, and every number is simulated.
A roof that decides bed by bed also keeps a record of what each bed was given.
No grower has seen this yet, and that is next."

### 1:22 to 1:30, the close, over the roof at night

"Elena still has one roof and one sky.
Now every bed gets its own answer."

Then two seconds of silence on the end card.

## The shot list, for the page as built

Every shot is a screen recording of the page at its own speed, at 1440 by 900 if the layout allows it, and never a phone pointed at a monitor.
The run is never sped up, and it is never cut between 09:00 and 17:00, because that stretch is the claim.

| # | Seconds | What is on the screen | How to get it |
|---|---|---|---|
| 1 | 0:00 to 0:21 | The roof in the Overview view at 00:00, three zones labelled, "Simulated, from historical weather inputs". The title card sits over the opening 4 seconds | Load the page, press Reset view, scroll to the top |
| 2 | 0:21 to 0:36 | One Flectofin module. Caption, burned in: "The fin is the Flectofin, by ITKE, University of Stuttgart, patent EP2320015. Not ours." | Press "Inspect a module" |
| 3 | 0:36 to 0:38 | The pointer on "Run the simulated day", one click | The button sits below the roof, so record the click, then cut |
| 4 | 0:38 to 0:59 | The run from 09:00 to 17:00, uncut, about 21.6 seconds. The fern's zone shuts 4.8 seconds in, the hydrangea's 7.2 seconds in, and the storm runs from 14.4 to 19.2 seconds in | Record a whole run with the roof in frame, and cut in at 09:00. The cut from the click to 09:00 is the one cut allowed |
| 5 | 0:59 to 1:08 | The storm, held: 15:00, rain 23.9 mm, the hydrangea's bays open, and the three decision reasons readable | Press "Go to the storm at 15:00". This is a still hold and not a slowed run. Caption: "15:00, held" |
| 6 | 1:08 to 1:22 | A zone's decision log, with its hours and its reasons in words. Caption, burned in: "Simulated. Rain from one real gauge, sun from a satellite product. Nothing physical was built." | Select the hydrangea's zone after the run, and scroll to its log |
| 7 | 1:22 to 1:30 | The roof at 23:00, shut. The end card: the closing line, then `github.com/andomo3/flecto-shade` and the team's names | The end of the run |

Why shot 5 exists: on the built page an hour of rain plays in 2.4 seconds, so the storm is on the screen for 4.8 seconds, and `story.md` found that too short to read three reasons.
The story asked for 5.0 seconds an hour, and the page was built without it, so the edit holds a still frame in its place.

Captions are burned in for every spoken line, because judges often watch with the sound off.
Where fifty crops is spoken, its source sits under it in small type: UF/IFAS, Apopka.
Where the football field is spoken, the caption gives the real figure and its source: "One gear motor will handle up to 50,000 sq ft of roof", UMass fact sheet on retractable roof greenhouses and shadehouses.
The football field is the team's comparison and not the source's: a field with its end zones is 57,600 square feet, so 50,000 is most of one.
The voice is recorded apart from the screen, in a quiet room, on a phone held close.

## If the farmer-selected watering flow merges before the recording

`AGENTS.md` calls that flow, in pull request 5, the intended primary interaction, and it is not on `main`.
If it is merged and works on `main` before the recording, it takes shots 5 and 6: the farmer picks two areas, the rain falls, and only their flaps admit it.
The words from 1:08 to 1:22 then become: "And the farmer can choose: pick the beds that are dry, and only their flaps take the rain. All of it is simulated, and no grower has seen it yet."
If it is not merged, it is not in the video, because the video shows what `main` does.

## The checks

PASS means the planner checked it against the file or the page today.
NOT YET means it cannot be checked until the recording exists, and it is never read as PASS.

### The skill's rules for a script

| Check | Result | Evidence |
|---|---|---|
| Opens with a story, and never with "hi, we are" | PASS | "Picture Elena" |
| The user is named within the opening two sentences | PASS | Sentence one |
| The problem is said in one sentence | PASS | "one curtain on one motor", so "every bed gets the same" |
| The pain is felt, in under 30 seconds | PASS | "Elena moves the plant", by 0:21 |
| The problem has its low before the product appears | PASS | 21 seconds before the turn |
| The demo starts by the 60 second mark | PASS | The click is at 0:36 |
| Three specifics in each sixty seconds | PASS | Fifty crops, thirty to ninety percent, most of a football field with 50,000 square feet in the caption, then eleven, noon, and forty two millimetres |
| The demo is a scene and not a tour | PASS | One day, one storm, no feature list, no stack |
| A wow moment is marked | PASS | Shot 5, one storm and three answers |
| What makes it different is said | PASS | "bed by bed", against one curtain over most of a football field |
| The close returns to the character, with no new information | PASS | Elena, the last two lines |
| The ask comes before the close | PASS | "and that is next" |
| Ends on the link, and stops | PASS | The end card, then silence |
| Inside the word range for its length | PASS | 233 words, range 225 to 270 |
| Nothing invented about users or evidence | PASS | No quote, no pilot, no user feedback claimed, and "no grower has seen this yet" is said |
| A proxy stays a proxy | PASS | Light and rain are said as light and rain, and no outcome for a crop is claimed |
| One concrete metric tied to a person | PARTLY | Forty two millimetres and three answers are tied to Elena's beds. The year's figure for the rain's share is left out, because `headline.json` does not exist |
| User testing or feedback mentioned | PASS, as an absence | Said plainly that there is none |

### The repo's release checklist, the pitch lines

| Check | Result | Evidence |
|---|---|---|
| The pitch matches the demonstrated behaviour | PASS | The planner ran the day on `main`: the fern's zone closes at 11:00, the hydrangea's at 12:00, the blueberries' stays open, and at 15:00 the hydrangea's opens for rain while the other two stay closed |
| Every numeric claim is reproduced | PASS | 42.4 mm over hours 15 and 16, and the hours 11 and 12, are in `software/page/day.json`. Fifty crops and 50,000 square feet are sourced in `story.md` |
| Observations, modelled inputs, simulation, and assumptions are told apart | PASS | "a real rain gauge, and a modelled sun", "all of it is simulated", and the caption on shot 6 |
| Credits are accurate | PASS | ITKE, University of Stuttgart, patent EP2320015, spoken and captioned |
| Two timed rehearsals and a fallback recording | NOT YET | Done on Sunday morning |

### The words the team never says

| Check | Result |
|---|---|
| None of the listed words is in the spoken text or the captions, as a claim | PASS. "Nothing was built" and "simulated" are the only words about evidence |
| No figure for cost, yield, energy, or water saved | PASS |
| Nothing says the roof prevents, reduces, or detects disease or salt build-up | PASS. The record is said as a record, and nothing more |
| The record is not called something no other shade house keeps | PASS. That wording was cut from the draft, because nobody checked it |

### Before it ships, from `video.md`

| Check | Result |
|---|---|
| Watched once with the sound off, and it still makes sense | NOT YET |
| Watched once by someone who has not seen the project, and they can say what it does | NOT YET |
| The voice read aloud with a timer, three times, and it lands inside 88 seconds | NOT YET |
| The link on the end card opens in a private window | NOT YET |
| The opening frame works as a thumbnail | NOT YET |

### The 30 point self assessment

Not scored, because it scores a delivery, and nothing has been delivered yet.
Score it after the third timed read.

## What the planner saw on the page, for the frontend's owner

These are not the script's to fix, and they will show in a recording.

- At a browser window about 1470 pixels wide, the page scrolls sideways, and the label of the zone at the left edge of the roof is cut off.
- "Run the simulated day" sits a full screen below the roof, so the click and the roof cannot be in one frame.
- The storm plays in 4.8 seconds, which is why shot 5 is a held frame.

## Where each figure came from

| Figure | File |
|---|---|
| Fifty crops, thirty to ninety percent shade, 50,000 square feet a motor | `story.md`, from the research notes it names |
| Eleven, noon, 42.4 mm in hours 15 and 16, the three reasons in the storm | `software/page/day.json`, from package H1 |
| 21.6, 4.8, 7.2, 14.4, and 19.2 seconds | the `play_seconds` of each hour in `software/page/day.json`, 0.5 at night and 2.4 by day |

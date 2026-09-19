# Pitch script

Cut from `planning/pitch/story.md` and `planning/pitch/script.md`, edited here for what the software actually does.
Speaker: abba drives, the judge presses Play.
`[X]` and `[Y]` are filled in from the result card after the measurement run, and until they are, nobody says a number out loud.

## 15 seconds, for a judge walking past

"A bus stop roof with no hinges that bends into shade when the sun hits it. Press play."

## 30 seconds

"Picture Rosa, waiting for a bus in Houston in July.
Researchers measured seventeen stops there, and found shelters that were hotter than standing in the open.
It trapped the heat, and it never moved, while the sun moves all day.
So we built a roof that moves: three leaves with no hinges, borrowed from a flower, that feel the sun and bend into shade on their own.
Press play, and watch one real Houston day in a minute.
With the leaves bent, the bench gets [X] percent of the light, against [Y] percent resting."

## 60 seconds

"Picture Rosa.
It is three in the afternoon in July, in Houston, and her bus is twelve minutes away.
Only about one in six stops in her city has a shelter.
And when researchers carried instruments to seventeen of those stops, they found the worst shelter was five degrees hotter than standing in the open.

Why would a roof make it worse?
It was closed in, and it trapped the heat.
And the sun moves all day, while a roof never does.

So we went looking for a roof that moves, and we found it in a flower.
The bird of paradise bends open with no hinge and no joint.
Our leaves do the same: one motor, three leaves, nothing to wear out.

Press play.
This is the third of June, a real Houston summer day from the European Commission's public solar dataset, run in a minute.
The data moves the sun.
The leaves move themselves: cover that sensor with your hand, and watch.

With the leaves bent, [X] percent of the light reaches the bench, against [Y] percent without.
We cannot move the sun.
So we built the roof that moves."

## 3 minutes

The long version in `planning/pitch/script.md` is unchanged except for three lines, which are said this way now:

- The day is named: "the third of June, from the European Commission's PVGIS typical year for Houston."
- The honesty line points at the screen: "the page tells you where every number came from, and it says 'not fitted' where we had no sensor."
- The proof line points at the bars: "the top bar is the light hitting the roof, the bottom bar is what reaches the bench, and the gap between them is the whole project."

## The sentences that keep it honest

- Measured: "We measured that today, on this table, with a sensor on the bench."
- Modelled: "The sun on this table is an LED playing a public solar dataset. That part is modelled, not measured."
- Replay mode on: "Right now the app is driving the leaves from recorded angles, because this room fools the sensor. The banner on the screen says so."
- Simulation source: "There is no board connected right now, and the screen says simulation. Here is the run we recorded with the board this morning."
- A sensor we never fitted: "That one says not fitted, because we did not fit it. It is not a zero."

## Recovery lines

- The leaves do not respond: "Rooms like this are bright, so let me trigger it by hand." Open the drawer, push the LED up, say it once.
- The board dies: "Here is this morning's run, recorded from the same sensors." Restart with `--source fixture`.
- The page shows the red banner before you do: read it out. "It just told you the cable died. That is the honest version of a demo."
- Everything dies: the backup clip, apologise once, keep telling Rosa's story over it.
- A question nobody can answer: "Good question. We did not get to that in twenty four hours, and here is how I would find out."

Opening line, memorised: "Picture Rosa. It is three in the afternoon in July, in Houston, and her bus is twelve minutes away."
Closing line, memorised: "We cannot move the sun. So we built the roof that moves instead."

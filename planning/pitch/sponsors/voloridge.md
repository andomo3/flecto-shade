# Voloridge: signal in the noise

Owner: abba speaks this one.
Written 2026-09-20 from the repository, and every figure below names the file it came from and whether it is reproduced by checked-in code.

## 1. What they ask for

[GAP. The official challenge text needs a login on the day-of prizes page, so it is not quoted here.
What is on record: the challenge is called "Signal in the Noise", and abba confirmed on Saturday evening that it accepts any dataset, which is why the project's own two public files qualify as they are.
abba pastes the real text here, and the sections below are then checked against it.]

## 2. Our one sentence

"The most valuable thing we found in our data was a signal that was not real, and catching it changed the dataset the whole project is built on."

## 3. How we attacked it

### The finding: we manufactured a false signal, and then detected it

An early build joined a typical meteorological year of sun, stitched from several years, to one real year of rain.
It is a standard move, and it produced a result that is physically impossible.

On real files, checked for another Gulf Coast site, the rainy daylight hours came out **brighter** than the dry ones, a ratio of **1.11**.
Rain was falling under a bright sky, because the sun and the rain had nothing to do with each other.

Taking the sun from the same place and the same year as the rain gives a ratio of **0.627**: rainy hours are dark hours, as they are outdoors.

That number is now an acceptance check in `planning/plans/packages/H1-zones-light-rain-soil.md`, "the mean `ghi` of rainy daylight hours over dry ones is 0.627 within 0.005", so it is reproduced every time the data is rebuilt and it cannot silently drift.

Why it matters for a decision system: our roof opens for rain and shuts for light.
Under the false join it would have seen bright, rainy afternoons that never happen, and learned the wrong policy from them.
The artifact was not in the model. It was in the join.

### Three more places the data lies, all found by looking

These came out of a study of the Florida Automated Weather Network, run by the University of Florida, in `planning/docs/research/flectofin-greenhouse-roof/agricultural-data-voloridge.md`.

**The satellite cannot see the difference we are selling.**
NASA POWER returns byte for byte identical irradiance for two stations 21 km apart, because both fall inside one grid cell of 0.5 by 0.625 degrees.
A project about differences between beds cannot take its light from a product that averages over 100 km, and saying that out loud is the point.

**Rain at 21 km is close to a coin flip.**
Of 557 hours wet at either Apopka or Avalon, only 205 were wet at both, 36.8 percent, with a bootstrap 95 percent interval of 32.7 to 40.9.
So a gauge is local, and a roof that acts on rain needs its own sensor, not a regional feed.

**The cleaning trap that leaves no trace.**
FAWN timestamps follow the local clock and shift with daylight saving.
Join them to POWER's UTC with a fixed five hour offset and the hourly RMSE is 175 W per square metre with r of 0.812.
Handle the shift and the same two files give 103 and 0.934.
The annual means agree either way, so nothing warns you: the only way to catch it is to look at the hours.

### What we did so a figure cannot drift

- Every dataset's provenance, byte count and sha256 are in `data/README.md`, so a judge can audit a claim built on public data.
- Five gate tests enforce the labelling. Gate F5 asserts that the word "measured" appears nowhere except the one line where it is true of the rain gauge. Gate F6 asserts that every assumed constant is declared with its value.
- Two runs of the same day produce identical bytes, asserted by gate F7.

## 4. The boundary, stated before anyone asks

The four FAWN figures above are the research author's provisional analysis, and **checked-in code does not yet reproduce them**.
The file says so on its own face, and so did the pull request that added it.
The 0.627 ratio is the exception: it is an acceptance check and it is reproduced on every build.

The 1.11 ratio is from another Gulf Coast site, not from the Apopka files the page uses, and the repository does not name that site or its year.
It is quoted as what the check showed, and never as a figure about Apopka.

## 5. Show, do not tell

Thirty seconds.

1. `data/README.md`, the section "Why the sun is from a real year and not a typical one". Point at 1.11 and 0.627.
2. `planning/plans/packages/H1-zones-light-rain-soil.md` line 120, the acceptance check. Say: that is why it cannot drift back.
3. `data/README.md`, the note that NASA's own precipitation column has 4,395 wet hours in 2023 where the gauge has 373, so we do not use it.
4. The FAWN file's own boundary line. Say: these four are provisional, and we have not reproduced them in code yet.

## 6. What we do not claim

- We do not claim a finding about crops, yield, disease or soil. The roof state disagreements are outputs of assumed control rules, not measurements of anything.
- We do not claim the FAWN figures are reproduced. They are provisional and the file says so.
- We do not claim 1.11 describes Apopka.
- We make no figure for water saved, cost, or energy, and the test suite fails the build if the page does.

## 7. Questions they will ask

**"What is the actual signal here?"**
"That the join was wrong, and the data told us so if we looked at the right slice.
Annual means looked fine in both the sun join and the daylight saving join. The artifact only showed up when we asked whether rainy hours were darker than dry ones, which is a question with a known physical answer.
That is the check we would run first on any new dataset now: find the relationship you already know the sign of, and see whether the data agrees."

**"How much of this is reproduced in code?"**
"One figure of the five, the 0.627 ratio, and it is an acceptance test.
The other four come from a research pass over the FAWN files and are labelled provisional in the repository and in the pull request that added them.
I would rather tell you which is which than present all five as equal."

**"Why these datasets?"**
"We were told any dataset qualifies, so we chose for auditability rather than for novelty.
One NOAA gauge, measured, and one NASA POWER product, modelled, both with their sha256 in the repository, for one place and one year so that the sun and the rain belong to each other.
The lesson from the 1.11 ratio is that the pairing matters more than the source."

## Where each figure came from

| Figure | Source | Reproduced by code? |
|---|---|---|
| Ratio 1.11, rainy hours brighter | `planning/plans/packages/S1-solar-2023.md` line 10, another Gulf Coast site, site and year not named in the repo | No, it is a record of a check |
| Ratio 0.627, rainy hours darker | `data/README.md` line 33, and the acceptance check at `H1-zones-light-rain-soil.md` line 120 | Yes, on every build |
| 36.8 percent, rain agreeing across 21 km, CI 32.7 to 40.9 | `agricultural-data-voloridge.md` | No, provisional |
| Byte identical irradiance for two stations in one cell | the same file | No, provisional |
| RMSE 175 to 103, r 0.812 to 0.934 with the DST fix | the same file | No, provisional |
| 4,395 satellite wet hours against the gauge's 373 | `data/README.md` lines 95 to 103 | Yes, it is why the column is unused |
| Dataset sha256 values and byte counts | `data/README.md` lines 17, 18, 24, 25 | Yes, checked on download |

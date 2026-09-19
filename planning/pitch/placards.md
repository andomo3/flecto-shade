# Placards

Four cards and a QR, printed or hand lettered at the event, standing on the table where a judge can read them without asking.
They do the work of a slide deck at a booth, and they keep the pitch honest while the speaker is mid sentence.
They are also the only things on the table beside the laptop, because nothing physical was built.
Large type, few words, readable from a metre.
Square brackets are filled in at the event, from `data/processed/headline.json` and never from memory.
The figures shown below in brackets are provisional, from the planner's run, and each is confirmed against `headline.json` before the card is made.

## Card 1: Simulated today

> **Simulated, not built**
>
> Near Apopka, Florida, through the year 2023.
> Rain: the Orlando Executive Airport gauge, NOAA.
> Sun: NASA POWER, a satellite product, modelled.
>
> Share of each zone's water that the rain supplied, simulated:
> Hydrangea: **[about 54] %**
> Blueberry: **[about 17] %**
> Boston fern: **0 %**, it opted out of rain.
>
> The fern held to its 8 mol light target on **[about 354]** of 365 days, simulated.

## Card 2: Not claimed

> **Not claimed**
>
> - Yield, cost, or water saved.
> - Safety from disease.
> - Wind or hail.
> - A built roof.
> Nothing physical was built.
> - That a grower wants it.
> We have not asked one yet.
>
> The soil and crop numbers are textbook coefficients with assumed bucket sizes.
> Shading blueberries is not Florida practice: that figure is from Washington State.

This card is the one judges remember, because almost nobody else has one.

## Card 3: Not ours

> **Not ours**
>
> The fin: the Flectofin, by ITKE, University of Stuttgart, with the University of Freiburg.
> Patent EP2320015.
> Watering by the sun's energy, and holding a daily light target: standard in greenhouse computers from Ridder, Hoogendoorn, Argus, and Priva.
> Moving roofs over crops: sold by Cravo and Sun'Agri.

## Card 4: Ours

> **Ours**
>
> Light by the bed, not by the bay.
> One element that shades, vents, and admits rain.
> Nine written rules: night, then rain, then light.
> No AI in the loop.
>
> Today one motor moves up to 50,000 sq ft of roof.
> Source: UMass fact sheet on retractable roof greenhouses and shadehouses.
>
> We found no prior proposal to put a Flectofin over crops.

The nine rules are printed in full on the back of this card, or on a sheet beside it, copied from `../plans/packages/H1-zones-light-rain-soil.md`.
The exact figures live on the cards, so the spoken pitch can round them.

## The QR

One code, to the event repo, whose README carries the video, the figures, the sources, and the link to the public planning repo.
Test it with two different phones.

## Making them

Card stock, a thick marker, and a ruler.
If the venue has a printer, print them, and if not, hand lettering reads as craft and not as a shortcut.
Cards 2, 3, and 4 can be worded now, and card 1 waits for `headline.json`.

## Where each figure came from

| Figure | File |
|---|---|
| 54 and 17 percent, 354 days, the 8 mol target | `../plans/packages/H1-zones-light-rain-soil.md`, provisional until `headline.json` exists |
| 50,000 sq ft a motor, and the makers on card 3 | `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md` |
| The patent and the two universities | `../docs/research/flectofin-design-tool/sector-choice.md` |
| The wording of the four cards | `../plans/pitch-plan-d.md` |

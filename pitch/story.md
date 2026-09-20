# A choice for each growing area

**One sentence:** For a shade-house grower choosing which areas need water, this simulation tests combinations of circular roof flaps that admit rain to the selected soil.

**Character, explicitly illustrative:** Imagine Sam, a grower near Apopka, Florida, with several growing areas under one roof. Sam wants rain on two areas while the others stay dry. This is a scenario, not an interview or a customer testimonial.

**Problem:** A roof opening covers a physical footprint. An opening that reaches the desired soil may also reach soil the grower wants to protect.

**Story spine:** Sam normally makes decisions for several growing areas. When rain arrives, Sam wants two of those areas watered. Sam selects them in our simulation. The controller finds permitted flap combinations, advances the rain event, and closes flaps as targets are reached. Sam can see where the request worked and where geometry or policy prevented it. The vision is a future roof that acts on these choices; this demo proves the software loop under stated assumptions.

**Arc:** A precise request → a physical coverage constraint → a visible combination of flap openings → accounted delivery → an honest limit → an invitation to validate the next experiment.

**Three specifics:** Apopka is the intended setting; the supplied CAD has 22 flap instances; the default two-footprint example meets 42 selected-cell targets. All water results are simulated. See generated [results](results.md) before speaking any number.

**Closing callback:** Sam starts by choosing two areas. We finish with those areas accounted for, and the roof closed again.

**Ask:** Help us find one grower and one physical test setup to compare the predicted footprint with actual rain reaching soil.

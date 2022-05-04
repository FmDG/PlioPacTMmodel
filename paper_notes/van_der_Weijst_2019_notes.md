# A Ternary Mixing Model Approach Using Benthic Foraminifer d13C - d18O Data to Reconstruct Late Pliocene Deep Atlantic Water Mass Mixing

**van der Weijst et al., 2019**

#Pliocene #NAtlantic #Models 

### Abstract
- Late Pliocene Atlantic $\delta^{13}$C data has been used for enhanced AMOC compared to present.
- This study combines $\delta^{13}$C and $\delta^{18}$O (which are both semi-conservative) to investigate.
- If you assume that the benthic $\delta^{13}$C-$\delta^{18}$O is mainly from mixing, you can determine the end-member states.
	- This requires three components, two from the North (NCW) and one from the South (SCW).
- Using a ternary mixing model, they suggest that the AMOC cell was deeper during M2 than during late Pliocene interglacials.
- There is also a cold, well-ventilated, water mass in the SE Atlantic between 3.6 and 2.7 Ma that did not contribute really to the rest of the basin (*could this be the PMOC incursion? [[Burls_2017]]*)
- The late Pliocene $\delta^{13}$C gradient between the NCW and SCW was similar to present day 1.1$\unicode{x2030}$.

## Paper
### Introduction
During the Late Pliocene, particularly the mPWP (3.264 - 3.025 Ma) there is a much warmer climate especially in the high-latitudes.

Previous studies have determined AMOC strength through $\delta^{13}$C of forams which is thought to represent $\delta^{13}\text{C}_{\text{DIC}}$ which can, as it is pretty conservative in the Atlantic Ocean, track water masses. This allows $\delta^{13}$C to track the degree of mixing between $^{13}$C-enriched deep water from the North Atlantic and Arctic (NCW) and $^{13}$C-depleted Southern Component Water (SCW). 

The complications with using $\delta^{13}$C as a conservative water mass tracer include the fact that it loses its conservative properties due to very low ventilation rates in the deep ocean (water mass aging) and local remineralisation in regions of high export productivity (such as the Southern Ocean).

Several studies, including [[Raymo_1992]], have used $\delta^{13}$C to point to increase late Pliocene AMOC strength. However, modelling results do not corroborate this.

The contribution of NCW and SCW to the deep Atlantic Ocean is often quantified using a binary mixing model (BMM) developed by [Oppo and Fairbanks, 1987](https://doi.org/10.1016/0012-821X(87)90183-X), and shown below:
$$
\displaylines{
\%\text{NCW} = 100 \times \left(\delta^{13}\text{C}_{(\text{Site})} - \delta^{13}\text{C}_{\text{(SCW endmember)}} \right) / \left( \delta^{13}\text{C}_{\text{(NCW endmember)}} - \delta^{13}\text{C}_{\text{(SCW endmember)}}\right) \\ 
\%\text{SCW}_{\text{(Site)}} = 100 - \%\text{NCW}
}
$$
The problems with this model is that it requires knowing the isotopic composition of the NCW and SCW endmembers - not often very easily done. It also assumes that there were only two endmembers which is likley not the case in the past.

For every benthic $\delta^{13}$C record, there exists a $\delta^{18}$O record. Foraminiferal $\delta^{18}$O reflects seawater and temperature - which are both conservative water mass properties. Therefore, they suggest using a Ternary Mixing Model (TMM) with both oxygen and carbon isotopes.

They also present new Late Pliocene oxygen and carbon isotope records for the deep Eastern Equatorial Atlantic as this is a major gap in the current data availability.

#### Water Masses in the Atlantic
The NCW is a mix of NEADW and NWADW. NEADW is relatively saline and warm, and consists mainly of Iceland Scotland Overflow Water (ISOW). NWADW is fresher but much cooler and is mainly Denmark Strait Overflow Water (DSOW) mixing with Labrador Sea Water (LSW). 

The SCW is mainly AABW, which is formed of Weddell Sea Bottom Water (WSBW), Ross Sea Bottom Water (RSBW) and Adélie Land Bottom Water (ALBW). 

North of the equator NADW occupies most of the Atlantic, but in abyssal waters (below 4000 m depth) there is still AABW up to 50$\degree$N in the modern ocean. South of the equator, abyssal waters are 50% AABW, while above 4000 m there is increasing AABW with increasing southward travel.

#### Endmember Composition
The end-member $\delta^{13}$C is mainly a product of surface producitivity and respiration, and sea water advection. The high $\delta^{13}$C signature of NCW results from preferential fixing of $^{12}$C during photosynthesis. 

Aging of water masses in the Atlantic is not a hugely important factor - but it is in the Pacific and Indian Oceans. This water is generally recirculated around Antarctica as CDW and gives the low $\delta^{13}$C of SCW. The influence of aging on the carbon isotopes are a function of the ventilation of the water mass.

Ocean $\delta^{18}$O is controlled by seawater temperature ($\delta^{18}\text{O}$ decreases by $\sim 0.25\unicode{x2030} / \celsius$ with increasing temperature), and by the $\delta^{18}$O$_\text{sw}$ in source regions. Variation in the $\delta^{18}$O$_\text{sw}$ reflects the balance between precipitation and evaporation, freshwater runoff, sea ice growth, melt processes, sea water advection, and the growth and decline of global ice sheets. 

### Methods
They follow the approach of [Bell et al. 2015](https://doi.org/10.1038/srep12252) who average the $\delta^{18}$O-$\delta^{13}$C over several time slices. They looked at seven separate time slices centred around the mPWP: three peak glacial stages (M2, KM2 and G20)), two phases of the mPWP (mPWP-1 and mPWP-2), and two bordering intervals. 

Time Slice | Age Bounds (ka)
---------------|-----------
3500 ka - M2 | 3500 - 3320
M2 | 3303 - 3288
mPWP-1 | 3280 - 3155
KM2 | 3148 - 3120
mPWP-2 | 3105 - 3030
G20 | 3025 - 3000
G20 - 2800 ka | 2985 - 2800

Most of the data was collected on *Cibicidoides wuellerstorfi* but there were corrections applied to those that were not.

The spread of the data they had indicated that they needed not one NCW endmember but two to describe the carbon and oxygen isotope space.

![[Screenshots/Figure_2.png]]

Pacific Ocean records are probably substantially affected by aging, markedly lowering the $\delta^{13}$C of the records from there. There may also have been a PMOC (as mentioned by [[Burls_2017]]), which would further complicate matters.

Rather than assign an endmember to a particular site, they estimated the location based on several sites. They also use the MinBoundSuite algorithm of [d'Errico, 2020](https://uk.mathworks.com/matlabcentral/fileexchange/34767-a-suite-of-minimal-bounding-objects) built in **MATLAB**. This was also run using the modern data from [Schmittner et al. 2017](https://doi.org/10.1002/2016PA003072). 







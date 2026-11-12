"""
DeepLeaf Comprehensive Plant Disease Knowledge Base
Covers all 38 classes of the PlantVillage / DeepLeaf model with authoritative
agricultural data, botanical taxonomy, symptoms, causes, organic and chemical treatments.
"""

DISEASE_KNOWLEDGE_BASE = {
    "Apple___Apple_scab": {
        "plant_name": "Apple",
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "disease_name": "Apple Scab",
        "status": "Diseased",
        "severity": "High",
        "pathogen_type": "Fungal",
        "causal_agent": "Venturia inaequalis",
        "description": "Apple scab is a widespread fungal disease affecting leaves and fruit. It creates dark, olive-green to black velvety scabs. Over time, affected leaves turn yellow and drop prematurely, severely reducing tree vigor, fruit quality, and market yield.",
        "symptoms": [
            "Olive-green, velvety, circular spots on the upper leaf surface",
            "Spots become dark brown, sunken, and corky over time",
            "Premature defoliation and stunted leaf growth",
            "Scabby, cracked lesions on apple fruit surfaces"
        ],
        "causes": [
            "Prolonged leaf wetness (6+ hours) in humid spring conditions (15-24°C)",
            "Overwintering fungal spores in fallen leaf litter on the orchard floor",
            "Dense, unpruned canopies that restrict rapid drying after rain"
        ],
        "immediate_actions": [
            "Rake, collect, and safely destroy fallen leaves and mummified fruit beneath trees",
            "Prune inner canopy branches to improve sunlight penetration and air circulation",
            "Avoid overhead irrigation; water strictly at the base or through drip lines"
        ],
        "organic_treatments": [
            "Liquid copper fungicide sprays applied during early bud break before blooms open",
            "Wettable sulfur sprays applied during early spring before infection periods",
            "Neem oil and potassium bicarbonate sprays for mild suppressive and protective action"
        ],
        "chemical_treatments": [
            "Apply protectant fungicides containing Captan, Mancozeb, or Difenoconazole according to local orchard spray schedules",
            "Apply early season sprays from green tip stage through petal fall for optimal protection"
        ],
        "prevention_tips": [
            "Plant scab-resistant apple cultivars such as Liberty, Freedom, or Enterprise",
            "Maintain strict autumn sanitation by shredding or composting fallen leaves with high nitrogen",
            "Ensure proper tree spacing (4-6 meters) for rapid canopy drying after rainfall"
        ],
        "fertilizer_and_care": [
            "Avoid excess nitrogen fertilizer in late spring, which stimulates susceptible tender shoots",
            "Apply balanced compost and mulch around the drip line, keeping mulch 10 cm away from the trunk"
        ]
    },

    "Apple___Black_rot": {
        "plant_name": "Apple",
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "disease_name": "Black Rot (Frogeye Leaf Spot)",
        "status": "Diseased",
        "severity": "Severe",
        "pathogen_type": "Fungal",
        "causal_agent": "Botryosphaeria obtusa",
        "description": "Black rot is a destructive fungal pathogen attacking foliage, twigs, and fruit. It causes distinctive 'frogeye' circular leaf spots, limb cankers, and dark mummified rotting apples that persist through winter.",
        "symptoms": [
            "Small purple leaf specks enlarging into circular spots with tan centers and purple margins ('frogeye')",
            "Sunken, reddish-brown to black cankers on branches and tree limbs",
            "Firm brown fruit rot with dark concentric rings, eventually shriveling into black mummies",
            "Blighted twigs and premature leaf yellowing"
        ],
        "causes": [
            "Fungal spores spreading from dead wood, pruning stubs, and mummified fruit during warm wet periods (20-27°C)",
            "Sunscald, fire blight injury, or winter freeze damage that creates open entry wounds"
        ],
        "immediate_actions": [
            "Prune out all dead wood, blighted twigs, and branch cankers at least 15 cm below infected tissue",
            "Remove and incinerate all mummified fruit clinging to branches or lying on the ground",
            "Disinfect pruning shears between cuts with 70% isopropyl alcohol or 10% bleach"
        ],
        "organic_treatments": [
            "Dormant copper sprays (Bordeaux mixture or copper octanoate) applied before bud swell",
            "Biofungicides containing Bacillus subtilis to protect fresh pruning cuts"
        ],
        "chemical_treatments": [
            "Fungicide sprays with Captan, Thiophanate-methyl, or Mancozeb from silver tip through harvest",
            "Apply protectant sprays within 24 hours of infection-favorable rain events"
        ],
        "prevention_tips": [
            "Protect bark from winter sunscald by painting lower trunks with white latex paint",
            "Conduct annual dormant-season pruning to eliminate old cankered wood and improve air movement",
            "Control leaf-feeding insects and fire blight to reduce bark wounds"
        ],
        "fertilizer_and_care": [
            "Maintain moderate tree vigor with balanced soil nutrition; avoid over-fertilizing with nitrogen"
        ]
    },

    "Apple___Cedar_apple_rust": {
        "plant_name": "Apple",
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "disease_name": "Cedar Apple Rust",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Gymnosporangium juniperi-virginianae",
        "description": "Cedar apple rust is a heteroecious fungus requiring both apple trees and Eastern red cedar (juniper) to complete its two-year life cycle. It causes brilliant yellow-orange leaf spots that can cause early defoliation.",
        "symptoms": [
            "Bright yellow-orange, circular spots on the upper leaf surface in late spring",
            "Spots enlarge with tiny black dots (pycnia) forming in the center",
            "Tubular, thread-like projections (aecia) appear on the underside of infected leaves",
            "Distorted, bumpy lesions on green fruit near the calyx end"
        ],
        "causes": [
            "Windborne spores traveling from gelatinous orange galls on nearby juniper/cedar trees during wet spring weather"
        ],
        "immediate_actions": [
            "Inspect nearby cedar/juniper trees within 500 meters and prune out brown galls if accessible",
            "Remove heavily spotted leaves on young or dwarf apple trees to reduce stress",
            "Keep canopy open to promote rapid leaf drying"
        ],
        "organic_treatments": [
            "Sulfur-based sprays applied just before apple blossom buds open",
            "Bacillus amyloliquefaciens biofungicide sprays during high-spore dispersal periods"
        ],
        "chemical_treatments": [
            "Myclobutanil (Immunox), Mancozeb, or Propiconazole applied from tight cluster through petal fall"
        ],
        "prevention_tips": [
            "Select rust-resistant apple varieties such as Redfree, Prima, Freedom, or William's Pride",
            "Remove wild Eastern red cedars adjacent to the orchard perimeter where feasible"
        ],
        "fertilizer_and_care": [
            "Maintain consistent soil moisture and apply balanced organic fertilizer in early spring"
        ]
    },

    "Apple___healthy": {
        "plant_name": "Apple",
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "disease_name": "Healthy Apple Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "The apple foliage is vibrant, healthy, and thriving. Leaves display uniform chlorophyll pigmentation, clean venation, and strong cell wall integrity without fungal or insect blemishes.",
        "symptoms": [
            "Crisp, uniform deep-green leaf blades with no chlorosis or necrosis",
            "Intact serrated leaf margins with no curling, spots, or powdery coating",
            "Sturdy new shoot growth and healthy terminal buds"
        ],
        "causes": [
            "Optimal growing conditions with proper sunlight, balanced nutrition, and appropriate soil moisture"
        ],
        "immediate_actions": [
            "No chemical or corrective treatment needed",
            "Continue regular monitoring and good orchard sanitation"
        ],
        "organic_treatments": [
            "Apply foliar seaweed extract or compost tea once a month to boost natural plant immunity"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Provide 25-35 mm of water weekly during dry periods using drip irrigation",
            "Apply dormant organic copper or horticultural oil spray in late winter to suppress overwintering pests"
        ],
        "fertilizer_and_care": [
            "Conduct annual soil testing to maintain soil pH between 6.0 and 6.8 with balanced micronutrients"
        ]
    },

    "Blueberry___healthy": {
        "plant_name": "Blueberry",
        "scientific_name": "Vaccinium corymbosum",
        "family": "Ericaceae",
        "disease_name": "Healthy Blueberry Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "The blueberry plant is healthy and vigorous with deep glossy green leaves, demonstrating excellent root uptake and ideal soil acidity.",
        "symptoms": [
            "Glossy, oval, deep-green leaves without marginal scorching or interveinal yellowing",
            "Healthy reddish-green cane growth and well-developed fruit buds"
        ],
        "causes": [
            "Well-maintained acidic soil (pH 4.5-5.2) with adequate organic matter and drainage"
        ],
        "immediate_actions": [
            "No disease management required"
        ],
        "organic_treatments": [
            "Mulch with 7-10 cm of aged pine bark or pine needles to preserve acidity and moisture"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Check soil pH every spring and apply elemental sulfur if pH rises above 5.2",
            "Use drip irrigation with non-alkaline water to prevent iron chlorosis"
        ],
        "fertilizer_and_care": [
            "Fertilize with ammonium sulfate or organic acid-loving plant fertilizer in split spring applications"
        ]
    },

    "Cherry_(including_sour)___Powdery_mildew": {
        "plant_name": "Cherry",
        "scientific_name": "Prunus avium / Prunus cerasus",
        "family": "Rosaceae",
        "disease_name": "Cherry Powdery Mildew",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Podosphaera clandestina",
        "description": "Powdery mildew attacks young cherry foliage and developing fruit, producing white powdery patches that cause leaf distortion, upward cupping, and reduced photosynthesis.",
        "symptoms": [
            "White, powdery fungal patches on leaves and tender young shoots",
            "Leaves curl upward, become distorted, brittle, and blistered",
            "Stunted terminal shoot growth and dull, scarred fruit skin"
        ],
        "causes": [
            "Warm days (18-28°C) combined with high relative humidity and poor canopy air circulation"
        ],
        "immediate_actions": [
            "Prune out crowded water sprouts and blighted shoot tips to open the canopy",
            "Increase sunlight exposure and improve air movement through the tree"
        ],
        "organic_treatments": [
            "Potassium bicarbonate (0.5%) or wettable sulfur sprays applied at first sign of white powder",
            "Dilute milk spray (1 part milk to 9 parts water) sprayed in direct sunlight as a preventative"
        ],
        "chemical_treatments": [
            "Myclobutanil, Trifloxystrobin, or Tebuconazole applied at petal fall and shuck split"
        ],
        "prevention_tips": [
            "Avoid high nitrogen fertilizer that promotes excessive susceptible young growth",
            "Plant trees in sunny, well-ventilated orchard sites"
        ],
        "fertilizer_and_care": [
            "Apply balanced fertilizer early in the season; stop nitrogen fertilization by mid-summer"
        ]
    },

    "Cherry_(including_sour)___healthy": {
        "plant_name": "Cherry",
        "scientific_name": "Prunus avium / Prunus cerasus",
        "family": "Rosaceae",
        "disease_name": "Healthy Cherry Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Healthy cherry foliage showing crisp, dark green leaves with distinct serrated edges, free of shot-hole damage, powdery mildew, or bacterial spots.",
        "symptoms": [
            "Deep green, glossy leaves with clean serrated margins",
            "Vigorous shoot growth and clean bark on fruiting spurs"
        ],
        "causes": [
            "Proper orchard sanitation, optimal soil drainage, and good light penetration"
        ],
        "immediate_actions": [
            "No treatment necessary"
        ],
        "organic_treatments": [
            "Apply foliar micronutrient spray with zinc and boron during post-harvest period"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Apply dormant organic copper spray in late autumn to protect against bacterial canker",
            "Maintain clean orchard floor free of fallen leaves and pruned twigs"
        ],
        "fertilizer_and_care": [
            "Keep soil evenly moist during fruit development; reduce watering post-harvest"
        ]
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "plant_name": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "family": "Poaceae",
        "disease_name": "Gray Leaf Spot (Cercospora)",
        "status": "Diseased",
        "severity": "High",
        "pathogen_type": "Fungal",
        "causal_agent": "Cercospora zeae-maydis",
        "description": "Gray leaf spot is one of the most economically damaging foliar diseases of maize. It produces long, narrow rectangular lesions restricted by leaf veins, leading to severe blighting and stalk lodging.",
        "symptoms": [
            "Small, tan spots expanding into long rectangular lesions (1-5 cm long) bounded by parallel veins",
            "Mature lesions turn grayish-tan with distinct yellow halos under backlighting",
            "Leaves dry out, turn brown, and die prematurely, causing poor grain filling and stalk breakage"
        ],
        "causes": [
            "Continuous warm, humid weather (24-30°C) with persistent morning dew or heavy fog",
            "Overwintering fungal mycelium in unburied corn residue from minimum-tillage fields"
        ],
        "immediate_actions": [
            "Scout corn fields from V12 through blister stage to measure canopy infection level",
            "Prioritize protecting the ear leaf and top three leaves responsible for grain filling"
        ],
        "organic_treatments": [
            "Rotate fields out of corn to non-host crops (soybeans, alfalfa, small grains) for at least 1-2 years",
            "Chop and incorporate surface corn residue post-harvest to speed decomposition"
        ],
        "chemical_treatments": [
            "Apply combination fungicides (Azoxystrobin + Propiconazole, Pyraclostrobin, or Fluoxastrobin) at VT (tasseling) to R2"
        ],
        "prevention_tips": [
            "Select maize hybrids with high genetic tolerance or resistance to Gray Leaf Spot",
            "Avoid planting continuous corn in fields with a history of severe leaf spot"
        ],
        "fertilizer_and_care": [
            "Ensure balanced potassium fertilization, which strengthens corn stalk rind and leaf cell walls"
        ]
    },

    "Corn_(maize)___Common_rust_": {
        "plant_name": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "family": "Poaceae",
        "disease_name": "Common Rust",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Puccinia sorghi",
        "description": "Common rust is an airborne fungal disease producing prominent cinnamon-brown to golden-brown pustules on both upper and lower leaf surfaces, reducing active green photosynthetic area.",
        "symptoms": [
            "Oval to elongated cinnamon-brown pustules (uredinia) scattered across both leaf surfaces",
            "Pustules rupture the leaf epidermis, releasing powdery rusty-brown spores when brushed",
            "Late in the season, pustules darken to brownish-black teliospores",
            "Severe infection causes premature yellowing, leaf necrosis, and reduced ear weight"
        ],
        "causes": [
            "Cool to moderate temperatures (16-25°C) combined with high relative humidity and night dews",
            "Windborne spores carried northwards from southern regions during spring weather fronts"
        ],
        "immediate_actions": [
            "Inspect ear leaves: if rust pustules cover >10% of leaf area before the blister stage, plan intervention",
            "Distinguish common rust from southern rust (southern rust has smaller orange pustules mainly on upper surface)"
        ],
        "organic_treatments": [
            "Sulfur dusts or biofungicides containing Bacillus subtilis for small-scale sweet corn gardens"
        ],
        "chemical_treatments": [
            "Triazole or Strobilurin fungicides (e.g., Pyraclostrobin, Tebuconazole, Azoxystrobin) applied when threshold is exceeded"
        ],
        "prevention_tips": [
            "Plant corn hybrids containing specific Rp gene resistance against Puccinia sorghi",
            "Plant early in the season to minimize exposure to late-summer rust spore influxes"
        ],
        "fertilizer_and_care": [
            "Provide balanced nitrogen and potassium; avoid moisture stress during silking"
        ]
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "plant_name": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "family": "Poaceae",
        "disease_name": "Northern Corn Leaf Blight",
        "status": "Diseased",
        "severity": "High",
        "pathogen_type": "Fungal",
        "causal_agent": "Exserohilum turcicum",
        "description": "Northern corn leaf blight causes large, elongated cigar-shaped grayish-green to tan lesions on corn leaves. Severe epidemics can destroy the leaf canopy and slash grain yields by up to 50%.",
        "symptoms": [
            "Large, elliptical, cigar-shaped lesions (3-15 cm long, 1-3 cm wide) on leaves",
            "Lesions start grayish-green, turning tan with dark fungal sporulation during wet periods",
            "Lesions merge, causing whole leaves to dry up and die prematurely ('scorched' look)"
        ],
        "causes": [
            "Moderate temperatures (18-27°C) with extended leaf wetness periods (6-18 hours)",
            "Fungal survival in infected corn residue from previous seasons"
        ],
        "immediate_actions": [
            "Evaluate leaf disease severity at reproductive stage (VT to R1)",
            "Protect the upper canopy leaves that provide sugar to developing kernels"
        ],
        "organic_treatments": [
            "Tillage to bury corn stover and accelerate microbial decomposition",
            "Two-year crop rotation with non-host broadleaf crops like soybeans"
        ],
        "chemical_treatments": [
            "Apply strobilurin or triazole fungicides (Azoxystrobin, Propiconazole, Pyraclostrobin) at first sign of lesions on lower leaves"
        ],
        "prevention_tips": [
            "Choose corn hybrids with polygenic and Ht-gene resistance against Exserohilum turcicum",
            "Practice proper crop rotation and avoid continuous zero-till corn in high-risk bottomland fields"
        ],
        "fertilizer_and_care": [
            "Maintain soil test-based fertility to ensure strong vegetative growth"
        ]
    },

    "Corn_(maize)___healthy": {
        "plant_name": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "family": "Poaceae",
        "disease_name": "Healthy Corn Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Healthy maize foliage showing broad, emerald-green leaves with strong central midribs, uniform pigmentation, and clean photosynthetic leaf area.",
        "symptoms": [
            "Broad, vigorous green leaves with clean midribs and unblemished margins",
            "Upright leaf architecture and strong stalk development without lodging"
        ],
        "causes": [
            "Adequate nitrogen, phosphorus, and moisture with favorable sunshine and weed management"
        ],
        "immediate_actions": [
            "Continue standard agronomic scouting and fertilization schedule"
        ],
        "organic_treatments": [
            "Sidedress with composted poultry manure or organic nitrogen at V6 growth stage"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Ensure proper plant population and row spacing for optimum canopy sunlight",
            "Scout weekly during tasseling and silking for early foliar disease signs"
        ],
        "fertilizer_and_care": [
            "Maintain adequate nitrogen supply; ensure soil moisture during pollination"
        ]
    },

    "Grape___Black_rot": {
        "plant_name": "Grape",
        "scientific_name": "Vitis vinifera / Vitis labrusca",
        "family": "Vitaceae",
        "disease_name": "Grape Black Rot",
        "status": "Diseased",
        "severity": "Severe",
        "pathogen_type": "Fungal",
        "causal_agent": "Guignardia bidwellii",
        "description": "Black rot is one of the most destructive fungal diseases of grapes in humid regions, attacking leaves, shoots, and fruit clusters. Berries turn into hard, black, raisin-like mummies.",
        "symptoms": [
            "Small, circular reddish-brown leaf spots with dark borders and tiny black pimple-like dots (pycnidia) in rings",
            "Berries develop pale brown spots that rapidly envelop the entire berry within 48 hours",
            "Infected fruit shrivels into hard, black, wrinkled mummies that cling to clusters",
            "Elongated black lesions on young green canes"
        ],
        "causes": [
            "Warm temperatures (21-27°C) accompanied by rain splash and high humidity in spring",
            "Overwintered mummified berries left hanging on vines or lying on the vineyard floor"
        ],
        "immediate_actions": [
            "Hand-pick and destroy all black mummified berries from vines and ground immediately",
            "Prune out infected green canes during the growing season and burn dead wood"
        ],
        "organic_treatments": [
            "Copper hydroxide or copper octanoate sprays applied from 2 cm shoot growth through post-bloom",
            "Biofungicide sprays containing Bacillus subtilis applied preventatively"
        ],
        "chemical_treatments": [
            "Apply Myclobutanil (Rally), Mancozeb, Captan, or Tebuconazole at pre-bloom, bloom, and post-bloom stages"
        ],
        "prevention_tips": [
            "Practice open-canopy trellis training and leaf pulling around clusters to ensure rapid drying",
            "Mow vineyard ground cover and keep vineyard rows free of tall weeds"
        ],
        "fertilizer_and_care": [
            "Avoid over-fertilizing with nitrogen which creates excessively dense, shaded canopies"
        ]
    },

    "Grape___Esca_(Black_Measles)": {
        "plant_name": "Grape",
        "scientific_name": "Vitis vinifera",
        "family": "Vitaceae",
        "disease_name": "Esca (Black Measles / Trunk Disease)",
        "status": "Diseased",
        "severity": "Severe",
        "pathogen_type": "Fungal Complex",
        "causal_agent": "Phaeomoniella chlamydospora & Phaeoacremonium minimum",
        "description": "Esca is a serious wood-rotting trunk disease affecting mature grapevines. It causes distinctive 'tiger-stripe' leaf patterns, berry spotting ('measles'), and in acute cases, sudden collapse of the entire vine (apoplexy).",
        "symptoms": [
            "'Tiger-stripe' foliar pattern: interveinal yellowing (white cultivars) or reddening (red cultivars) that dries into brown necrosis with green veins",
            "Dark purple to black specks ('measles') on berry skin, accompanied by cracked, shriveled fruit",
            "Spongy white heart rot in the center of vine trunks and cordons",
            "Sudden vine wilting and death (apoplexy) during hot summer spells"
        ],
        "causes": [
            "Fungal infection entering through large pruning wounds during wet winter weather",
            "Spread through infected vine nursery wood or unsterilized pruning equipment"
        ],
        "immediate_actions": [
            "Mark symptomatic vines during summer for targeted renewal or double-pruning in winter",
            "Prune out diseased cordons at least 15 cm into clean, healthy wood"
        ],
        "organic_treatments": [
            "Apply Trichoderma-based bio-protectants directly onto fresh pruning wounds within 24 hours of cutting"
        ],
        "chemical_treatments": [
            "Seal large pruning wounds with pruning sealant containing Thiophanate-methyl or boron pastes"
        ],
        "prevention_tips": [
            "Delay pruning until late winter or early spring when wounds heal much faster",
            "Never prune vines during rain or when rain is forecast within 48 hours",
            "Disinfect pruning shears regularly with 70% alcohol or bleach solution"
        ],
        "fertilizer_and_care": [
            "Retain vine balance with moderate irrigation; avoid extreme heat stress"
        ]
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "plant_name": "Grape",
        "scientific_name": "Vitis vinifera",
        "family": "Vitaceae",
        "disease_name": "Leaf Blight (Isariopsis)",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Pseudocercospora clavispora (Phaeoisariopsis vitis)",
        "description": "Leaf blight causes irregular, angular brown spots on grape leaves that can lead to extensive late-season defoliation, reducing winter hardiness and next year's fruit bud differentiation.",
        "symptoms": [
            "Irregular, angular dark brown necrotic spots on leaves, often limited by small veins",
            "Velvety, dark olive-brown to black spore tufts on the underside of spots in humid weather",
            "Yellow halo surrounding lesions; leaves turn yellow, curl upward, and drop prematurely"
        ],
        "causes": [
            "Warm, humid summer conditions with dense canopy shade and poor airflow"
        ],
        "immediate_actions": [
            "Rake and destroy fallen leaves post-harvest to reduce overwintering fungal spores",
            "Thin out lateral shoots to increase sunlight penetration into the interior canopy"
        ],
        "organic_treatments": [
            "Copper oxychloride or Bordeaux mixture sprays applied after harvest and during early spring"
        ],
        "chemical_treatments": [
            "Mancozeb, Ziram, or Chlorothalonil sprays applied on a 10-14 day interval"
        ],
        "prevention_tips": [
            "Maintain proper vertical shoot positioning (VSP) trellis architecture",
            "Pull leaves around the fruit zone after berry set for maximum air velocity"
        ],
        "fertilizer_and_care": [
            "Ensure adequate potassium levels to enhance foliar cuticle resistance"
        ]
    },

    "Grape___healthy": {
        "plant_name": "Grape",
        "scientific_name": "Vitis vinifera",
        "family": "Vitaceae",
        "disease_name": "Healthy Grapevine Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "The grapevine foliage is healthy and vigorous. Leaves display uniform deep green color with sharp lobes, clean venation, and active shoot tip growth with tendrils.",
        "symptoms": [
            "Vibrant, dark green palmate leaves free from spots, discoloration, or curling",
            "Sturdy cane growth and healthy flowering/fruiting clusters"
        ],
        "causes": [
            "Proper canopy management, balanced soil moisture, and timely preventative care"
        ],
        "immediate_actions": [
            "Maintain standard viticultural shoot positioning and leaf pulling practices"
        ],
        "organic_treatments": [
            "Apply foliar seaweed or amino acid sprays to enhance natural vine stress resistance"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Monitor weekly for early signs of downy mildew, powdery mildew, or leafhoppers",
            "Keep vineyard understory mowed to discourage humidity buildup"
        ],
        "fertilizer_and_care": [
            "Maintain balanced N-P-K fertility with attention to magnesium and potassium"
        ]
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        "plant_name": "Orange (Citrus)",
        "scientific_name": "Citrus sinensis",
        "family": "Rutaceae",
        "disease_name": "Huanglongbing (Citrus Greening / HLB)",
        "status": "Diseased",
        "severity": "Critical",
        "pathogen_type": "Bacterial",
        "causal_agent": "Candidatus Liberibacter asiaticus",
        "description": "Huanglongbing (HLB) is one of the most destructive citrus diseases worldwide. Transmitted by the Asian citrus psyllid, it clogs the tree's phloem vascular system, causing asymmetric leaf mottling, yellow shoots, and bitter, misshapen fruit that remains green at the base.",
        "symptoms": [
            "Blotchy, asymmetric mottling on leaves (patterns do not match on opposite sides of midrib)",
            "Yellowing of leaf veins resembling severe zinc or iron micronutrient deficiency",
            "Small, lopsided, bitter fruit with dark aborted seeds; fruit stays green at the blossom end ('greening')",
            "Twig dieback, heavy premature fruit drop, and overall decline of tree vigor"
        ],
        "causes": [
            "Bacterial infection delivered directly into phloem sieve tubes by the Asian citrus psyllid (Diaphorina citri)"
        ],
        "immediate_actions": [
            "Scout tree for Asian citrus psyllid adults (feeding at 45-degree angle) and nymphs (white waxy honeydew)",
            "Report suspected cases to local agricultural extension service",
            "Remove and destroy severely infected trees to prevent infecting neighboring groves"
        ],
        "organic_treatments": [
            "Horticultural mineral oils or neem extract sprays to deter psyllid feeding and egg laying",
            "Release beneficial biocontrol parasitoid wasps (Tamarixia radiata) where available"
        ],
        "chemical_treatments": [
            "Strict psyllid vector control with Imidacloprid, Thiamethoxam, or Cyantraniliprole",
            "Intensive foliar nutritional sprays (zinc, manganese, iron, boron) to sustain tree productivity"
        ],
        "prevention_tips": [
            "Purchase only certified disease-free citrus trees grown in insect-proof screenhouses",
            "Install insect screen barriers and monitor groves with yellow sticky traps"
        ],
        "fertilizer_and_care": [
            "Provide frequent, light fertigation with balanced micronutrients to reduce root stress"
        ]
    },

    "Peach___Bacterial_spot": {
        "plant_name": "Peach",
        "scientific_name": "Prunus persica",
        "family": "Rosaceae",
        "disease_name": "Peach Bacterial Spot",
        "status": "Diseased",
        "severity": "High",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas arboricola pv. pruni",
        "description": "Bacterial spot attacks leaves, twigs, and fruit of peach trees. It causes angular purple-black lesions that drop out to create a 'shot-hole' appearance, leading to severe defoliation and cracked fruit.",
        "symptoms": [
            "Small, angular, water-soaked dark purple to black spots on leaves, concentrated along midrib and tips",
            "Dead centers drop out, leaving a ragged 'shot-hole' effect",
            "Leaves turn chlorotic (yellow) and drop prematurely; trees may lose 50%+ of leaves",
            "Dark, sunken, pitted cracks and gumming on peach fruit surfaces"
        ],
        "causes": [
            "Driving rains, high winds, and blowing sand that cause microscopic leaf abrasions",
            "Warm temperatures (21-29°C) with persistent moisture and dew"
        ],
        "immediate_actions": [
            "Avoid pruning or cultivating in the orchard during damp, rainy weather",
            "Eliminate overhead sprinkler watering that splashes bacteria between trees"
        ],
        "organic_treatments": [
            "Fixed copper sprays applied during dormant season (bud swell) and post-harvest",
            "Biobactericides with Bacillus amyloliquefaciens applied during early shoot growth"
        ],
        "chemical_treatments": [
            "Oxytetracycline (Mycoshield) or copper bactericides applied at low rates from petal fall through shuck split"
        ],
        "prevention_tips": [
            "Plant resistant peach cultivars (e.g., Candor, Dixired, Sentinel, Biscoe, Reliance)",
            "Plant windbreaks around sandy sites to minimize wind-blown sand abrasion"
        ],
        "fertilizer_and_care": [
            "Avoid excessive nitrogen fertilization that produces tender, succulent tissue prone to infection"
        ]
    },

    "Peach___healthy": {
        "plant_name": "Peach",
        "scientific_name": "Prunus persica",
        "family": "Rosaceae",
        "disease_name": "Healthy Peach Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Healthy peach leaves showing long, slender, lanceolate foliage with glossy deep-green surfaces, crisp finely serrated margins, and vigorous shoot extension.",
        "symptoms": [
            "Smooth, elongated green leaves free of spots, holes, curling, or yellowing",
            "Clean branch bark and healthy developing fruit without blemishes"
        ],
        "causes": [
            "Proper orchard management, good drainage, and preventative dormant-season disease control"
        ],
        "immediate_actions": [
            "Continue routine orchard watering and monitoring"
        ],
        "organic_treatments": [
            "Apply aged compost mulch around drip line, keeping root flare clear"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Apply dormant copper or lime-sulfur spray in late autumn to prevent peach leaf curl",
            "Thin fruit clusters in early summer to prevent branch breakage and maximize fruit size"
        ],
        "fertilizer_and_care": [
            "Maintain soil pH between 6.0 and 6.5; provide consistent irrigation during fruit swelling"
        ]
    },

    "Pepper,_bell___Bacterial_spot": {
        "plant_name": "Bell Pepper",
        "scientific_name": "Capsicum annuum",
        "family": "Solanaceae",
        "disease_name": "Bell Pepper Bacterial Spot",
        "status": "Diseased",
        "severity": "High",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas campestris pv. vesicatoria",
        "description": "Bacterial spot is a damaging disease of peppers causing small water-soaked foliar spots that turn brown and necrotic. It leads to rapid defoliation, exposing peppers to severe sunscald.",
        "symptoms": [
            "Small, water-soaked, circular to angular dark green or brown spots on leaves",
            "Spots develop light brown necrotic centers with dark borders, slightly raised on undersides",
            "Severe yellowing and premature leaf drop, leaving plants severely defoliated",
            "Rough, circular, cracked, blister-like spots on green and ripe peppers"
        ],
        "causes": [
            "Warm, wet weather (24-30°C), driving rains, overhead sprinkler irrigation, and infected seeds"
        ],
        "immediate_actions": [
            "Remove and safely destroy heavily infected plants; do not compost",
            "Never work or prune in pepper rows while foliage is wet",
            "Switch from overhead watering to drip irrigation or soaker hoses"
        ],
        "organic_treatments": [
            "Fixed copper bactericide (copper hydroxide or copper octanoate) applied every 7-10 days",
            "Biobactericides containing Bacillus subtilis or Bacillus amyloliquefaciens"
        ],
        "chemical_treatments": [
            "Tank-mix copper hydroxide with Mancozeb for enhanced bacterial control and resistance prevention"
        ],
        "prevention_tips": [
            "Use certified disease-free, hot-water-treated seed or resistant pepper varieties (X1-X10 resistant)",
            "Practice a 3-year crop rotation avoiding all Solanaceae crops (peppers, tomatoes, potatoes, eggplants)"
        ],
        "fertilizer_and_care": [
            "Apply balanced fertilizer; avoid excess nitrogen that prolongs vegetative susceptibility"
        ]
    },

    "Pepper,_bell___healthy": {
        "plant_name": "Bell Pepper",
        "scientific_name": "Capsicum annuum",
        "family": "Solanaceae",
        "disease_name": "Healthy Bell Pepper Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Lush, dark green bell pepper leaves showing smooth surfaces, intact margins, active vegetative growth, and healthy flowering nodes.",
        "symptoms": [
            "Uniform, glossy green leaves without spots, mottling, or curling",
            "Sturdy central stems and healthy white blossoms setting fruit"
        ],
        "causes": [
            "Warm growing conditions, well-draining soil, and consistent drip irrigation"
        ],
        "immediate_actions": [
            "Continue balanced watering and support plants with stakes or cages"
        ],
        "organic_treatments": [
            "Foliar fish-kelp fertilizer spray once every two weeks"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Maintain clean straw or plastic mulch to prevent soil splashing onto lower foliage",
            "Provide consistent moisture to prevent blossom end rot"
        ],
        "fertilizer_and_care": [
            "Ensure adequate calcium and magnesium in soil; maintain soil pH between 6.2 and 6.8"
        ]
    },

    "Potato___Early_blight": {
        "plant_name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "family": "Solanaceae",
        "disease_name": "Potato Early Blight",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Alternaria solani",
        "description": "Early blight is a widespread fungal disease attacking older potato foliage. It produces diagnostic 'bullseye' concentric rings on leaves, causing premature defoliation and smaller tuber yields.",
        "symptoms": [
            "Small, dark brown to black circular spots starting on oldest lower leaves",
            "Spots enlarge up to 1-2 cm showing characteristic concentric ring pattern ('target board')",
            "Surrounding leaf tissue turns yellow (chlorotic); leaves wither and drop",
            "Dark, sunken, dry circular lesions on potato tubers with purplish margins"
        ],
        "causes": [
            "Alternating wet and dry weather, plant stress (drought, low nitrogen), and warm temperatures (24-29°C)",
            "Fungal spores surviving on crop debris and volunteer potato plants"
        ],
        "immediate_actions": [
            "Prune off heavily infected lower leaves and remove them from the field",
            "Irrigate in the early morning so foliage dries rapidly before evening"
        ],
        "organic_treatments": [
            "Copper-based fungicides applied at first sign of target spots on lower canopy",
            "Biofungicide sprays containing Bacillus amyloliquefaciens"
        ],
        "chemical_treatments": [
            "Chlorothalonil, Mancozeb, Azoxystrobin, or Difenoconazole applied on 7-14 day intervals"
        ],
        "prevention_tips": [
            "Plant certified disease-free seed potatoes",
            "Ensure adequate nitrogen and potassium throughout the season to minimize plant stress",
            "Practice a 3-4 year crop rotation away from solanaceous crops"
        ],
        "fertilizer_and_care": [
            "Hill potatoes well to shield tubers from spores washing down through soil"
        ]
    },

    "Potato___Late_blight": {
        "plant_name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "family": "Solanaceae",
        "disease_name": "Potato Late Blight",
        "status": "Diseased",
        "severity": "Critical",
        "pathogen_type": "Oomycete",
        "causal_agent": "Phytophthora infestans",
        "description": "Late blight is the devastating water-mold organism that caused the Great Irish Famine. It spreads explosively in cool, wet weather, destroying entire potato fields within days and causing foul tuber rot.",
        "symptoms": [
            "Large, irregular, water-soaked dark green to purplish-black lesions on leaves",
            "White, cottony downy fungal growth visible on leaf undersides in high humidity/dew",
            "Rapid stem blackening, collapse of the vine canopy, and strong rotting odor",
            "Granular, reddish-brown dry rot extending under potato tuber skins"
        ],
        "causes": [
            "Cool, wet weather (10-21°C), relative humidity >90%, and persistent fog, mist, or rain"
        ],
        "immediate_actions": [
            "Act immediately upon detection; inspect the entire potato patch",
            "Cut and destroy infected haulms; do NOT compost blighted foliage",
            "Destroy all volunteer potato plants and cull piles nearby"
        ],
        "organic_treatments": [
            "Preventative copper hydroxide sprays applied thoroughly before disease emergence"
        ],
        "chemical_treatments": [
            "Apply Mandipropamid (Revus), Cymoxanil, Fluopicolide, or Metalaxyl/Mefenoxam with strict adherence to resistance guidelines"
        ],
        "prevention_tips": [
            "Plant late-blight-resistant potato cultivars (e.g., Sarpo Mira, Defender, Elba)",
            "Purchase only certified pathogen-free seed potatoes; destroy all cull potatoes"
        ],
        "fertilizer_and_care": [
            "Hill soil deeply over tubers to prevent sporangia from washing into root zones"
        ]
    },

    "Potato___healthy": {
        "plant_name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "family": "Solanaceae",
        "disease_name": "Healthy Potato Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Vigorous, rich green potato compound foliage with strong upright stems, clean leaflet surfaces, and active tuberization underground.",
        "symptoms": [
            "Uniform deep-green leaflets without spots, blights, or curling",
            "Sturdy haulms and healthy flower clusters"
        ],
        "causes": [
            "Well-draining sandy loam soil, proper hilling, and consistent moisture"
        ],
        "immediate_actions": [
            "Maintain standard hilling and weed management practices"
        ],
        "organic_treatments": [
            "Apply foliar seaweed extract once every 3 weeks to enhance root growth"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Keep potato tubers well-covered with soil to prevent greening (solanine) and spore contact",
            "Scout plants twice weekly during cool, overcast weather"
        ],
        "fertilizer_and_care": [
            "Ensure adequate potassium and phosphorus for optimal tuber bulking"
        ]
    },

    "Raspberry___healthy": {
        "plant_name": "Raspberry",
        "scientific_name": "Rubus idaeus",
        "family": "Rosaceae",
        "disease_name": "Healthy Raspberry Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Healthy raspberry foliage showing crisp green upper leaf surfaces with silvery-green undersides, sharp serrations, and sturdy cane growth.",
        "symptoms": [
            "Clean, serrated green leaves without yellowing, rust, or anthracnose lesions",
            "Vigorous primocanes and productive floricanes with healthy fruit clusters"
        ],
        "causes": [
            "Well-drained soil, adequate sun exposure, and good cane thinning practices"
        ],
        "immediate_actions": [
            "Maintain cane trellising and root watering"
        ],
        "organic_treatments": [
            "Apply aged wood chip mulch to conserve moisture and suppress weeds"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Prune out spent floricanes to the ground immediately after harvest to maximize airflow",
            "Ensure trellised canes are spaced 10-15 cm apart"
        ],
        "fertilizer_and_care": [
            "Apply balanced organic compost in early spring before new primocanes emerge"
        ]
    },

    "Soybean___healthy": {
        "plant_name": "Soybean",
        "scientific_name": "Glycine max",
        "family": "Fabaceae",
        "disease_name": "Healthy Soybean Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Healthy trifoliate soybean foliage with rich green color, intact margins, and active symbiotic nitrogen fixation in root nodules.",
        "symptoms": [
            "Vibrant green trifoliate leaves without mottling, rust pustules, or frogeye leaf spots",
            "Strong stem nodes setting healthy green pods"
        ],
        "causes": [
            "Adequate soil phosphorus, potassium, and active Bradyrhizobium nodulation"
        ],
        "immediate_actions": [
            "Continue standard crop monitoring"
        ],
        "organic_treatments": [
            "Inoculate soybean seed with Bradyrhizobium japonicum before planting"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Maintain crop rotation with corn, wheat, or sorghum to break pest/pathogen cycles",
            "Monitor soil fertility to avoid potassium deficiency"
        ],
        "fertilizer_and_care": [
            "Maintain soil pH between 6.0 and 6.8 for optimal nutrient availability"
        ]
    },

    "Squash___Powdery_mildew": {
        "plant_name": "Squash",
        "scientific_name": "Cucurbita pepo",
        "family": "Cucurbitaceae",
        "disease_name": "Squash Powdery Mildew",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Podosphaera xanthii / Erysiphe cichoracearum",
        "description": "Powdery mildew is a ubiquitous fungal disease of squash and cucurbits. It blankets leaves in white powdery fungal colonies, causing leaves to yellow, wither, and prematurely senesce.",
        "symptoms": [
            "White, talcum-like powdery spots on both upper and lower leaf surfaces and petioles",
            "Spots rapidly expand to cover the entire leaf blade",
            "Infected leaves turn yellow, become brittle and brown, and die prematurely",
            "Exposed squash fruit suffers sunscald and has reduced sugar content"
        ],
        "causes": [
            "Warm temperatures (20-27°C), dense foliage, shaded conditions, and moderate humidity",
            "Unlike downy mildew, powdery mildew does NOT require free standing water to infect"
        ],
        "immediate_actions": [
            "Prune out and discard heavily covered older leaves to slow fungal spore spread",
            "Space vines and prune surrounding weeds to maximize sunlight and airflow"
        ],
        "organic_treatments": [
            "Potassium bicarbonate spray (3 g per liter of water) with a few drops of liquid soap",
            "Neem oil or horticultural oil spray (1%) applied early morning or late afternoon",
            "Dilute milk spray (10-20% milk in water) sprayed on leaves in direct sunlight"
        ],
        "chemical_treatments": [
            "Myclobutanil, Trifloxystrobin, or Difenoconazole applied on a 7-10 day schedule"
        ],
        "prevention_tips": [
            "Select squash varieties with genetic resistance/tolerance to powdery mildew",
            "Avoid planting squash in heavily shaded garden corners"
        ],
        "fertilizer_and_care": [
            "Avoid excessive nitrogen that stimulates soft, dense, susceptible foliage"
        ]
    },

    "Strawberry___Leaf_scorch": {
        "plant_name": "Strawberry",
        "scientific_name": "Fragaria × ananassa",
        "family": "Rosaceae",
        "disease_name": "Strawberry Leaf Scorch",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Diplocarpon earlianum",
        "description": "Leaf scorch produces numerous small, irregular dark purple to reddish-purple spots that merge, making strawberry leaves appear burned or scorched, leading to reduced berry yield.",
        "symptoms": [
            "Numerous small, irregular purple to dark red spots without clear white centers",
            "Spots coalesce, causing leaf margins to curl upward and turn brown and scorched",
            "Infected fruit calyxes turn brown and dry out, degrading fruit marketability"
        ],
        "causes": [
            "Frequent rainfall, overhead sprinkler irrigation, and temperatures between 15-25°C"
        ],
        "immediate_actions": [
            "Remove and destroy infected leaves during bed renovation after harvest",
            "Switch immediately from overhead sprinklers to drip irrigation tape"
        ],
        "organic_treatments": [
            "Copper-based fungicides applied in early spring as new growth starts and post-harvest"
        ],
        "chemical_treatments": [
            "Captan, Thiophanate-methyl, or Pyraclostrobin sprays"
        ],
        "prevention_tips": [
            "Plant resistant strawberry cultivars",
            "Maintain wide plant spacing and keep beds weed-free for rapid leaf drying"
        ],
        "fertilizer_and_care": [
            "Apply straw mulch beneath plants to keep foliage and berries off damp soil"
        ]
    },

    "Strawberry___healthy": {
        "plant_name": "Strawberry",
        "scientific_name": "Fragaria × ananassa",
        "family": "Rosaceae",
        "disease_name": "Healthy Strawberry Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Healthy trifoliate strawberry foliage showing rich, deep green coloration, distinct serrated margins, active crowns, and vigorous runner production.",
        "symptoms": [
            "Uniform, glossy green leaves without purple spots, angular lesions, or mildew",
            "Healthy white flowers and plump developing green berries"
        ],
        "causes": [
            "Clean straw mulch, proper crown planting depth, and drip irrigation"
        ],
        "immediate_actions": [
            "Maintain clean mulch beneath plants and remove dead leaves"
        ],
        "organic_treatments": [
            "Apply compost tea or fish hydrolysate around the root zone"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Renovate June-bearing beds annually after harvest to promote fresh foliage",
            "Ensure strawberry crowns are planted level with the soil surface (not buried)"
        ],
        "fertilizer_and_care": [
            "Fertilize with balanced organic berry fertilizer in early spring and post-harvest"
        ]
    },

    "Tomato___Bacterial_spot": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Tomato Bacterial Spot",
        "status": "Diseased",
        "severity": "High",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas perforans / Xanthomonas vesicatoria",
        "description": "Bacterial spot produces small, dark, water-soaked lesions on tomato leaves, stems, and fruit. It causes extensive defoliation, exposing fruit to sunscald and reducing yield.",
        "symptoms": [
            "Small (1-3 mm), dark, angular water-soaked spots on leaves",
            "Lesion centers turn brown and die, often surrounded by a noticeable yellow halo",
            "Leaves turn scorched and drop, starting from the lower canopy upward",
            "Fruit develops small, dark, raised, scabby spots with rough surfaces"
        ],
        "causes": [
            "Warm, wet weather (24-30°C), driving rains, overhead irrigation, and contaminated seeds/transplants"
        ],
        "immediate_actions": [
            "Remove and destroy severely infected plants; do not compost",
            "Never touch, prune, or harvest tomato plants while leaves are wet",
            "Switch to drip irrigation to keep foliage completely dry"
        ],
        "organic_treatments": [
            "Fixed copper bactericide (copper hydroxide) applied every 7-10 days",
            "Biobactericide sprays containing Bacillus amyloliquefaciens"
        ],
        "chemical_treatments": [
            "Tank-mix copper hydroxide with Mancozeb for superior bacterial control and resistance management"
        ],
        "prevention_tips": [
            "Use certified pathogen-free, hot-water-treated seed or disease-tolerant varieties",
            "Practice a 3-year crop rotation avoiding all Solanaceae crops"
        ],
        "fertilizer_and_care": [
            "Apply straw or plastic mulch to prevent rain-splashed soil bacteria from hitting lower leaves"
        ]
    },

    "Tomato___Early_blight": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Tomato Early Blight",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Alternaria solani",
        "description": "Early blight is a very common fungal disease producing distinctive 'target board' concentric rings on leaves and dark sunken stem cankers, progressively defoliating plants from the bottom up.",
        "symptoms": [
            "Dark brown to black circular spots with distinctive concentric rings ('target board') on older lower leaves",
            "Yellow chlorotic halo around each lesion; leaves yellow, dry up, and drop",
            "Dark, sunken, leathery cankers on stems and near the fruit calyx",
            "Progressive defoliation moving upwards, exposing tomato fruit to sunscald"
        ],
        "causes": [
            "Warm temperatures (24-29°C) with alternating wet and dry conditions; soil-splashed spores"
        ],
        "immediate_actions": [
            "Prune off all lower infected leaves (up to 30-45 cm above ground level)",
            "Apply thick organic mulch (straw or paper) around plant base to prevent soil splash",
            "Water only at the root base using soaker hoses or drip tape"
        ],
        "organic_treatments": [
            "Copper fungicide or biofungicide (Bacillus subtilis) applied preventatively",
            "Potassium bicarbonate spray to suppress spore germination"
        ],
        "chemical_treatments": [
            "Chlorothalonil, Mancozeb, Azoxystrobin, or Difenoconazole applied at 7-14 day intervals"
        ],
        "prevention_tips": [
            "Stake, cage, or trellis tomato plants to keep foliage elevated off the soil",
            "Rotate tomato planting beds away from potatoes, eggplants, and peppers for 3 years"
        ],
        "fertilizer_and_care": [
            "Provide balanced fertilizer; avoid severe nitrogen deficiency which accelerates early blight"
        ]
    },

    "Tomato___Late_blight": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Tomato Late Blight",
        "status": "Diseased",
        "severity": "Critical",
        "pathogen_type": "Oomycete",
        "causal_agent": "Phytophthora infestans",
        "description": "Late blight is a catastrophic water-mold disease that can destroy healthy tomato plants in less than a week during cool, wet weather. It affects all foliage, stems, and fruit.",
        "symptoms": [
            "Large, irregular, water-soaked pale to dark green lesions on leaves that rapidly turn greasy brown/black",
            "Delicate white, cottony fungal growth visible on leaf undersides in high humidity and morning dew",
            "Stems develop dark brown to black greasy-looking cankers",
            "Fruit develops hard, bumpy, dark olive-brown greasy rot"
        ],
        "causes": [
            "Cool, rainy, or foggy weather (15-22°C) with persistent humidity >90%; windblown sporangia"
        ],
        "immediate_actions": [
            "Act immediately upon detection; remove and bag entire infected plants on a dry day",
            "Dispose of infected vines in sealed trash bags (do NOT compost)",
            "Alert neighboring growers as spores travel miles on the wind"
        ],
        "organic_treatments": [
            "Fixed copper sprays applied thoroughly as a preventative before infection establishes"
        ],
        "chemical_treatments": [
            "Mandipropamid (Revus), Cymoxanil, Chlorothalonil, or Fluopicolide applied immediately"
        ],
        "prevention_tips": [
            "Plant late-blight-resistant tomato cultivars (e.g., Defiant, Mountain Magic, Iron Lady, Plum Regal)",
            "Maximize plant spacing (at least 90 cm) to accelerate canopy drying after rainfall"
        ],
        "fertilizer_and_care": [
            "Drip irrigate early in the day; avoid overhead sprinklers at all costs"
        ]
    },

    "Tomato___Leaf_Mold": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Tomato Leaf Mold",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Passalora fulva (Cladosporium fulvum)",
        "description": "Leaf mold is a fungal disease that thrives in high-humidity greenhouse and tunnel environments, producing pale yellow spots on upper leaf surfaces and velvety olive-green mold underneath.",
        "symptoms": [
            "Pale yellow, diffuse chlorotic spots on the upper leaf surface",
            "Dense, olive-green to brown velvety fungal mold on the corresponding lower leaf surface",
            "Leaves curl, wither, turn brown, and drop prematurely, progressing upward through the canopy"
        ],
        "causes": [
            "High relative humidity (>85%), temperatures between 21-24°C, and poorly ventilated structures"
        ],
        "immediate_actions": [
            "Open greenhouse/tunnel vents and run circulation fans to reduce relative humidity below 80%",
            "Prune lower suckers and dense foliage to allow free airflow through the canopy"
        ],
        "organic_treatments": [
            "Copper octanoate or potassium bicarbonate sprays",
            "Biofungicide sprays containing Bacillus subtilis"
        ],
        "chemical_treatments": [
            "Chlorothalonil, Difenoconazole, or Azoxystrobin applied preventatively"
        ],
        "prevention_tips": [
            "Grow resistant tomato cultivars (with Cf resistance genes) in high tunnels and greenhouses",
            "Water with drip tape at the soil line; avoid late-afternoon irrigation that causes night condensation"
        ],
        "fertilizer_and_care": [
            "Maintain balanced nutrition; avoid excess foliage growth from over-fertilizing with nitrogen"
        ]
    },

    "Tomato___Septoria_leaf_spot": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Septoria Leaf Spot",
        "status": "Diseased",
        "severity": "High",
        "pathogen_type": "Fungal",
        "causal_agent": "Septoria lycopersici",
        "description": "Septoria leaf spot is one of the most destructive foliar diseases of tomatoes in humid climates, producing hundreds of tiny circular spots with gray centers and black dots, causing rapid defoliation.",
        "symptoms": [
            "Numerous small (2-4 mm), circular spots starting on the oldest lower leaves",
            "Spots have dark brown borders with distinctive gray or white centers",
            "Tiny black pimple-like fruiting bodies (pycnidia) visible inside spot centers",
            "Heavily infected leaves turn yellow, wither, and drop, leaving stems bare and fruit vulnerable"
        ],
        "causes": [
            "Splashing rain, warm temperatures (20-25°C), and wet foliage for extended periods"
        ],
        "immediate_actions": [
            "Prune off all infected bottom leaves and dispose away from the garden",
            "Apply clean straw or plastic mulch around tomato bases to block soil-to-leaf spore splashing",
            "Water exclusively at soil level with drip irrigation"
        ],
        "organic_treatments": [
            "Copper fungicide or sulfur sprays applied every 7-10 days",
            "Bacillus subtilis biofungicides applied at first sign of lower leaf spotting"
        ],
        "chemical_treatments": [
            "Chlorothalonil or Mancozeb applied preventatively at first cluster flowering"
        ],
        "prevention_tips": [
            "Stake or cage tomatoes and maintain at least 30 cm ground clearance for lower foliage",
            "Practice a 3-year crop rotation away from solanaceous plants"
        ],
        "fertilizer_and_care": [
            "Avoid overhead watering; remove all tomato debris at the end of the season"
        ]
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Two-Spotted Spider Mites",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Pest",
        "causal_agent": "Tetranychus urticae",
        "description": "Microscopic arachnid pests that pierce tomato leaf cells and suck out chlorophyll, causing fine yellow stippling, bronze discoloration, silken webbing, and premature leaf drop.",
        "symptoms": [
            "Fine yellow or white stippling on the upper surface of tomato leaves",
            "Leaves turn bronze, yellow, and dry, taking on a dusty, scorched appearance",
            "Delicate silken webbing visible on leaf undersides and around new shoot tips",
            "Tiny moving yellowish-green dots with two dark spots visible under magnification"
        ],
        "causes": [
            "Hot, dry, dusty weather (30-38°C) and pesticide overuse that eliminates natural predatory mites"
        ],
        "immediate_actions": [
            "Spray leaf undersides with a strong jet of water to knock down mites and webs",
            "Prune and discard heavily webbed branches in sealed bags"
        ],
        "organic_treatments": [
            "Insecticidal soap or horticultural oil (1%) applied thoroughly to leaf undersides",
            "Neem oil or rosemary oil sprays",
            "Release beneficial predatory mites (Phytoseiulus persimilis or Neoseiulus californicus)"
        ],
        "chemical_treatments": [
            "Miticides like Abamectin, Bifenazate, or Spiromesifen (follow harvest interval labels carefully)"
        ],
        "prevention_tips": [
            "Hose down garden paths and surrounding areas to minimize dust buildup",
            "Avoid broad-spectrum synthetic pyrethroids that kill natural mite predators"
        ],
        "fertilizer_and_care": [
            "Keep tomato plants well-watered to prevent drought stress that attracts spider mites"
        ]
    },

    "Tomato___Target_Spot": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Tomato Target Spot",
        "status": "Diseased",
        "severity": "Moderate",
        "pathogen_type": "Fungal",
        "causal_agent": "Corynespora cassiicola",
        "description": "Target spot produces circular brown lesions on leaves and fruit, often with faint concentric rings. It causes defoliation and sunken, pitted fruit blemishes.",
        "symptoms": [
            "Small, circular brown lesions with faint concentric rings and dark margins",
            "Lesions expand up to 10 mm; surrounding tissue turns yellow and falls off",
            "Sunken, dark circular lesions on green and ripe tomato fruit"
        ],
        "causes": [
            "Warm, humid conditions (20-28°C) with dense, unpruned plant canopies"
        ],
        "immediate_actions": [
            "Remove lower infected leaves to slow upward progression",
            "Prune suckers to enhance sunlight penetration and canopy ventilation"
        ],
        "organic_treatments": [
            "Copper-based protectant sprays applied every 7-10 days",
            "Biofungicides containing Bacillus amyloliquefaciens"
        ],
        "chemical_treatments": [
            "Chlorothalonil, Boscalid, or Azoxystrobin"
        ],
        "prevention_tips": [
            "Stake tomatoes and maintain at least 60-90 cm plant spacing",
            "Rotate crops with non-susceptible plants"
        ],
        "fertilizer_and_care": [
            "Water with drip tape; maintain balanced soil potassium and calcium"
        ]
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "status": "Diseased",
        "severity": "Critical",
        "pathogen_type": "Viral",
        "causal_agent": "Tomato yellow leaf curl virus (Begomovirus)",
        "description": "A devastating viral disease transmitted by silverleaf whiteflies. It causes severe stunting, upward leaf cupping, yellowing margins, and near-total crop loss if contracted early.",
        "symptoms": [
            "Pronounced upward curling and cupping of leaflets",
            "Severe chlorosis (yellowing) along leaf margins and interveinal areas",
            "Leaves become small, thick, leathery, and crumpled",
            "Extreme plant stunting with an erect, bushy appearance ('bonsai' look)",
            "Heavy blossom drop; plants fail to set fruit"
        ],
        "causes": [
            "Transmission by silverleaf whiteflies (Bemisia tabaci) within 15-30 minutes of feeding"
        ],
        "immediate_actions": [
            "Remove and destroy infected plants immediately; plant viruses cannot be cured once systemic",
            "Enclose infected plants in plastic bags before pulling to prevent whiteflies from scattering"
        ],
        "organic_treatments": [
            "Install yellow sticky cards to monitor and trap whitefly populations",
            "Insecticidal soap or neem oil sprays targeting whiteflies on leaf undersides",
            "Use floating row covers on young transplants to block whitefly access"
        ],
        "chemical_treatments": [
            "Systemic insecticides (e.g., Imidacloprid, Dinotefuran) to control the whitefly vector"
        ],
        "prevention_tips": [
            "Grow TYLCV-resistant tomato cultivars (e.g., Tycoon, Camaro, Chef's Choice Orange)",
            "Eradicate broadleaf weeds around field borders that act as alternative virus hosts"
        ],
        "fertilizer_and_care": [
            "Provide regular care to uninfected plants; destroy all infected crop residue post-harvest"
        ]
    },

    "Tomato___Tomato_mosaic_virus": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Tomato Mosaic Virus (ToMV)",
        "status": "Diseased",
        "severity": "Severe",
        "pathogen_type": "Viral",
        "causal_agent": "Tomato mosaic virus (Tobamovirus)",
        "description": "An exceptionally stable and highly contagious plant virus spread mechanically on hands, tools, and clothing. It causes mottled foliage, leaf distortion, and internal browning of fruit.",
        "symptoms": [
            "Mottled light and dark green mosaic patchwork pattern on leaves",
            "Leaves become distorted, puckered, blistered, or narrow ('shoestring' appearance)",
            "Stunted plant growth and uneven fruit ripening",
            "Internal brown necrotic rings inside the tomato fruit wall"
        ],
        "causes": [
            "Mechanical transmission via hands, pruning shears, stakes, seeds, and tobacco products"
        ],
        "immediate_actions": [
            "Immediately rogue out and destroy infected plants; do not touch healthy plants after touching an infected one",
            "Disinfect all pruning shears, stakes, and cages in a 10% bleach solution or 20% non-fat dry milk solution"
        ],
        "organic_treatments": [
            "No chemical or organic cure exists for viral infection; strict sanitation is the only control",
            "Wash hands thoroughly with soap and warm water or milk before handling tomato plants"
        ],
        "chemical_treatments": [
            "None effective against plant viruses"
        ],
        "prevention_tips": [
            "Choose certified virus-free seed with Tm-2 or Tm-2^2 genetic resistance",
            "Never smoke or handle tobacco products around tomato crops (tobacco carries mosaic viruses)"
        ],
        "fertilizer_and_care": [
            "Maintain separate tools for infected areas; destroy all crop residue at season's end"
        ]
    },

    "Tomato___healthy": {
        "plant_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "disease_name": "Healthy Tomato Foliage",
        "status": "Healthy",
        "severity": "None",
        "pathogen_type": "None",
        "causal_agent": "None",
        "description": "Healthy tomato foliage showing lush, deep-green compound leaves with aromatic foliage, sturdy stems, active blossom sets, and no signs of spots, curling, or blight.",
        "symptoms": [
            "Robust, vibrant green leaves with clean serrated margins and natural leaf texture",
            "Thick, sturdy stems and healthy yellow flower clusters setting fruit"
        ],
        "causes": [
            "Proper trellising, balanced soil moisture, consistent calcium uptake, and good air circulation"
        ],
        "immediate_actions": [
            "Continue regular watering and pruning of lower suckers for optimal canopy structure"
        ],
        "organic_treatments": [
            "Apply calcium-rich foliar spray and compost tea every 2-3 weeks"
        ],
        "chemical_treatments": [
            "None required"
        ],
        "prevention_tips": [
            "Mulch with straw or shredded leaves to prevent soil splash onto lower foliage",
            "Water deeply and consistently at the soil line to prevent blossom end rot"
        ],
        "fertilizer_and_care": [
            "Maintain soil pH between 6.2 and 6.8; apply balanced tomato fertilizer with adequate calcium"
        ]
    }
}


def get_disease_details(disease_key):
    """
    Look up comprehensive information for a disease class.
    Falls back gracefully to formatted strings if key is unknown.
    """
    if disease_key in DISEASE_KNOWLEDGE_BASE:
        data = dict(DISEASE_KNOWLEDGE_BASE[disease_key])
        data["class_key"] = disease_key
        return data

    # Fallback for unexpected or custom classes
    parts = disease_key.split("___") if "___" in disease_key else [disease_key, "Condition"]
    plant = parts[0].replace("_", " ").strip()
    disease = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Unknown Condition"
    is_healthy = "healthy" in disease.lower()

    return {
        "class_key": disease_key,
        "plant_name": plant,
        "scientific_name": f"{plant} sp.",
        "family": "Plantae",
        "disease_name": disease,
        "status": "Healthy" if is_healthy else "Diseased",
        "severity": "None" if is_healthy else "Moderate",
        "pathogen_type": "None" if is_healthy else "Pathogen",
        "causal_agent": "None" if is_healthy else "Identified by DeepLeaf AI",
        "description": f"Model identified {disease} on {plant}. Regular monitoring and cultural care recommended.",
        "symptoms": [
            f"Foliar patterns consistent with {disease}",
            "Visual changes in leaf texture or coloration"
        ],
        "causes": [
            "Environmental conditions favorable to plant disease development"
        ],
        "immediate_actions": [
            "Inspect neighboring plants for similar symptoms",
            "Prune any visibly damaged foliage and avoid overhead watering"
        ],
        "organic_treatments": [
            "Apply copper-based or neem-based organic protective spray if disease progresses"
        ],
        "chemical_treatments": [
            "Consult a local agricultural extension specialist for approved regional treatments"
        ],
        "prevention_tips": [
            "Maintain good plant spacing and sanitation",
            "Water early in the day to allow leaves to dry"
        ],
        "fertilizer_and_care": [
            "Provide balanced soil nutrition and maintain consistent moisture"
        ]
    }


SUPPORTED_CROPS = [
    {"name": "Apple", "scientific": "Malus domestica", "diseases_count": 4, "icon": "🍎"},
    {"name": "Blueberry", "scientific": "Vaccinium corymbosum", "diseases_count": 1, "icon": "🫐"},
    {"name": "Cherry", "scientific": "Prunus avium", "diseases_count": 2, "icon": "🍒"},
    {"name": "Corn (Maize)", "scientific": "Zea mays", "diseases_count": 4, "icon": "🌽"},
    {"name": "Grape", "scientific": "Vitis vinifera", "diseases_count": 4, "icon": "🍇"},
    {"name": "Orange", "scientific": "Citrus sinensis", "diseases_count": 1, "icon": "🍊"},
    {"name": "Peach", "scientific": "Prunus persica", "diseases_count": 2, "icon": "🍑"},
    {"name": "Bell Pepper", "scientific": "Capsicum annuum", "diseases_count": 2, "icon": "🫑"},
    {"name": "Potato", "scientific": "Solanum tuberosum", "diseases_count": 3, "icon": "🥔"},
    {"name": "Raspberry", "scientific": "Rubus idaeus", "diseases_count": 1, "icon": "🫐"},
    {"name": "Soybean", "scientific": "Glycine max", "diseases_count": 1, "icon": "🌱"},
    {"name": "Squash", "scientific": "Cucurbita pepo", "diseases_count": 1, "icon": "🎃"},
    {"name": "Strawberry", "scientific": "Fragaria × ananassa", "diseases_count": 2, "icon": "🍓"},
    {"name": "Tomato", "scientific": "Solanum lycopersicum", "diseases_count": 10, "icon": "🍅"},
]

HERB_DIAGNOSTIC_GUIDE = {
    "mint": {
        "title": "Mint (Pudina / Mentha) Care & Diagnosis Guide",
        "description": "Mint is an aromatic herb from the Lamiaceae family. DeepLeaf AI's core model was trained on 14 major agricultural crops (PlantVillage dataset). Because mint leaves feature serrated margins and purplish/reddish undertones, the neural network approximates it to Strawberry or Bell Pepper.",
        "common_conditions": [
            {
                "name": "Natural Stem & Leaf Pigmentation (Normal Anthocyanin)",
                "symptoms": "Reddish, purplish, or bronze shading on mint stems and lower leaves without wilting or necrotic spots.",
                "action": "Harmless and natural in peppermint (Mentha × piperita) and tulsi exposed to sunlight or cool temperatures. No treatment required."
            },
            {
                "name": "Mint Rust (Puccinia menthae)",
                "symptoms": "Small dusty orange, yellow, or reddish-brown pustules on the leaf undersides. Affected leaves turn yellow and drop prematurely.",
                "action": "Prune infected stems back to the soil line. Water at the base without splashing leaves. Spray organic neem oil or sulfur fungicide if rust spreads."
            },
            {
                "name": "Powdery Mildew (Golovinomyces / Erysiphe)",
                "symptoms": "White powdery talcum-like coating on mint leaf surfaces, causing leaf curling and drying.",
                "action": "Ensure full sunlight and good air circulation. Spray dilute baking soda (1 tsp per liter of water with 2 drops soap) or neem oil."
            },
            {
                "name": "Spider Mites / Aphid Feeding",
                "symptoms": "Tiny pale yellow pinprick specks on leaf surfaces, sometimes with fine delicate webs beneath leaves.",
                "action": "Rinse leaf undersides with a gentle spray of water. Spray with organic insecticidal soap or diluted neem oil."
            }
        ]
    },
    "tulsi": {
        "title": "Tulsi (Holy Basil / Ocimum) Care & Diagnosis Guide",
        "description": "Tulsi is widely grown in home gardens. Krishna Tulsi naturally has dark purple foliage and stems that can be mistaken by AI for disease discoloration.",
        "common_conditions": [
            {
                "name": "Natural Purple Coloration",
                "symptoms": "Deep purple stems and veins across leaves.",
                "action": "Normal healthy characteristic of Krishna Tulsi varieties, not a disease."
            },
            {
                "name": "Overwatering & Root Suffocation",
                "symptoms": "Lower leaves turn yellow and drop; soil remains soggy.",
                "action": "Allow the top 2 inches of soil to dry between waterings. Use a pot with good drainage holes."
            }
        ]
    }
}



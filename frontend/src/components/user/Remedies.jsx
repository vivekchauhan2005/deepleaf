import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { FaLeaf, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import { motion } from 'framer-motion';
 
const diseaseGuidance = [
  {
    match: 'apple___apple_scab',
    name: 'Apple Scab',
    cause: 'A fungal disease favored by wet foliage and humid spring weather.',
    symptoms: 'Olive or dark spots on leaves; lesions may also appear on fruit.',
    actions: [
      'Remove fallen infected leaves and dispose of them appropriately.',
      'Prune as needed to improve airflow and reduce prolonged leaf wetness.',
      'Ask a local horticulture expert about a registered apple-scab treatment.'
    ],
    prevention: 'Improve orchard sanitation and avoid overhead watering where practical.'
  },
  {
    match: 'apple___black_rot',
    name: 'Apple Black Rot',
    cause: 'A fungal pathogen that can survive in infected branches and plant debris.',
    symptoms: 'Leaf spots, dead twigs, or dark fruit rot.',
    actions: [
      'Remove mummified fruit and infected dead branches where practical.',
      'Disinfect pruning tools between affected plants.',
      'Seek crop-specific advice before using a fungicide.'
    ],
    prevention: 'Maintain orchard sanitation and monitor leaves, branches, and fruit.'
  },
  {
    match: 'apple___cedar_apple_rust',
    name: 'Cedar Apple Rust',
    cause: 'A fungal disease that alternates between susceptible apple trees and junipers.',
    symptoms: 'Orange-yellow leaf spots, sometimes with raised structures underneath.',
    actions: [
      'Inspect the tree and nearby susceptible host plants for signs of rust.',
      'Remove severely affected fallen leaves where practical.',
      'Ask an orchard specialist about local management options and timing.'
    ],
    prevention: 'Monitor trees during wet spring weather and maintain good airflow.'
  },
  {
    match: 'cherry___powdery_mildew',
    name: 'Cherry Powdery Mildew',
    cause: 'A fungal disease favored by susceptible new growth and suitable humidity.',
    symptoms: 'White, powdery growth on leaves and distorted young shoots.',
    actions: [
      'Remove badly affected growth where practical.',
      'Avoid excessive nitrogen fertilization that encourages soft new growth.',
      'Use only a treatment registered for cherry powdery mildew if advised locally.'
    ],
    prevention: 'Maintain airflow and monitor new growth regularly.'
  },
  {
    match: 'corn___cercospora_leaf_spot',
    name: 'Corn Gray Leaf Spot',
    cause: 'A fungal disease that can persist in infected corn residue.',
    symptoms: 'Long rectangular gray or tan lesions between leaf veins.',
    actions: [
      'Inspect neighboring plants for similar lesions.',
      'Manage infected crop residue using locally recommended crop practices.',
      'Ask an agricultural adviser whether a registered treatment is justified.'
    ],
    prevention: 'Use locally recommended resistant hybrids and crop rotation where suitable.'
  },
  {
    match: 'corn___common_rust',
    name: 'Corn Common Rust',
    cause: 'A fungal disease spread by airborne spores.',
    symptoms: 'Small reddish-brown raised pustules on leaves.',
    actions: [
      'Monitor how rapidly pustules are appearing and spreading.',
      'Check crop growth stage and disease severity before considering treatment.',
      'Consult local agricultural guidance for a suitable rust-management option.'
    ],
    prevention: 'Use resistant hybrids where available and scout the crop regularly.'
  },
  {
    match: 'corn___northern_leaf_blight',
    name: 'Northern Corn Leaf Blight',
    cause: 'A fungal disease that survives in infected crop residue.',
    symptoms: 'Long, cigar-shaped gray-green or tan leaf lesions.',
    actions: [
      'Check whether lesions are expanding on multiple leaves.',
      'Manage crop residue and rotation according to local recommendations.',
      'Ask an agricultural adviser about resistant hybrids and treatment options.'
    ],
    prevention: 'Choose locally recommended resistant hybrids and monitor humid periods.'
  },
  {
    match: 'grape___black_rot',
    name: 'Grape Black Rot',
    cause: 'A fungal disease that can persist in dried infected berries and other debris.',
    symptoms: 'Brown leaf spots and berries that shrivel into dark mummies.',
    actions: [
      'Remove dried infected berries and affected plant debris.',
      'Improve canopy airflow with appropriate vineyard management.',
      'Ask a vineyard specialist about preventive treatment timing.'
    ],
    prevention: 'Maintain vineyard sanitation and monitor during warm, wet weather.'
  },
  {
    match: 'grape___esca',
    name: 'Grape Esca',
    cause: 'A complex grapevine trunk disease associated with fungal pathogens.',
    symptoms: 'Striped or scorched-looking leaves, dieback, or affected wood.',
    actions: [
      'Mark affected vines and monitor symptoms over time.',
      'Avoid pruning during wet conditions where practical and protect large pruning wounds according to local guidance.',
      'Have a vineyard specialist inspect the vine; leaf images alone cannot confirm Esca.'
    ],
    prevention: 'Use sound pruning practices and suitable clean planting material.'
  },
  {
    match: 'grape___leaf_blight',
    name: 'Grape Leaf Blight',
    cause: 'A leaf disease associated with fungal infection and favorable wet conditions.',
    symptoms: 'Brown or dark lesions that may spread across leaf tissue.',
    actions: [
      'Remove fallen infected leaves where practical.',
      'Improve canopy airflow and avoid unnecessary leaf wetness.',
      'Confirm the cause with a local vineyard specialist before selecting treatment.'
    ],
    prevention: 'Maintain canopy management and vineyard sanitation.'
  },
  {
    match: 'orange___haunglongbing',
    name: 'Citrus Greening (Huanglongbing)',
    cause: 'A bacterial disease spread by Asian citrus psyllids.',
    symptoms: 'Uneven yellowing, blotchy leaves, and potentially misshapen fruit.',
    actions: [
      'Contact local agricultural or plant-health authorities for confirmation.',
      'Inspect for citrus psyllids with help from a qualified adviser.',
      'Do not expect ordinary fungicides to cure this bacterial disease.'
    ],
    prevention: 'Use certified planting material and follow local psyllid and disease-control guidance.'
  },
  {
    match: 'peach___bacterial_spot',
    name: 'Peach Bacterial Spot',
    cause: 'A bacterial disease favored by warm, wet conditions and rain splash.',
    symptoms: 'Small dark leaf spots that may develop angular holes or yellowing.',
    actions: [
      'Avoid working with wet foliage and reduce splash where practical.',
      'Remove badly affected fallen debris where appropriate.',
      'Ask a local fruit-tree specialist about resistant varieties and registered options.'
    ],
    prevention: 'Use locally recommended varieties and avoid unnecessary leaf wetness.'
  },
  {
    match: 'pepper,_bell___bacterial_spot',
    name: 'Pepper Bacterial Spot',
    cause: 'A bacterial disease spread through infected material, water splash, and handling.',
    symptoms: 'Small water-soaked or dark spots that may become rough or yellow-edged.',
    actions: [
      'Avoid handling plants when wet and sanitize tools between plants.',
      'Remove badly affected debris and avoid saving seed from suspect plants.',
      'Ask a local horticulture adviser about resistant seed and registered management options.'
    ],
    prevention: 'Use clean seed or transplants, rotate crops, and avoid overhead irrigation.'
  },
  {
    match: 'potato___early_blight',
    name: 'Potato Early Blight',
    cause: 'A fungal disease often favored by leaf wetness and plant stress.',
    symptoms: 'Brown lower-leaf spots that may show concentric rings.',
    actions: [
      'Remove badly affected leaves when practical without stripping the plant.',
      'Water at soil level and avoid prolonged leaf wetness.',
      'Ask a local adviser about potato-specific registered treatments if disease is progressing.'
    ],
    prevention: 'Rotate crops, manage plant debris, and maintain appropriate plant nutrition.'
  },
  {
    match: 'potato___late_blight',
    name: 'Potato Late Blight',
    cause: 'A destructive disease favored by cool to mild, humid conditions and leaf wetness.',
    symptoms: 'Fast-spreading water-soaked dark lesions, sometimes with pale growth underneath.',
    actions: [
      'Seek prompt local agricultural advice because the disease can spread rapidly.',
      'Avoid moving wet suspect foliage or tubers between plants and storage areas.',
      'Follow local guidance for handling infected plants and any registered treatment.'
    ],
    prevention: 'Use healthy seed tubers, monitor local blight alerts, and avoid prolonged leaf wetness.'
  },
  {
    match: 'squash___powdery_mildew',
    name: 'Squash Powdery Mildew',
    cause: 'A fungal disease affecting cucurbits, often visible on mature leaves.',
    symptoms: 'White powder-like patches on leaf surfaces.',
    actions: [
      'Remove severely affected leaves when practical.',
      'Maintain spacing and airflow without stressing the plant.',
      'If needed, ask a local adviser for a treatment registered for squash powdery mildew.'
    ],
    prevention: 'Monitor leaves regularly and use resistant varieties where available.'
  },
  {
    match: 'strawberry___leaf_scorch',
    name: 'Strawberry Leaf Scorch',
    cause: 'A fungal leaf disease that can persist in infected strawberry debris.',
    symptoms: 'Small purple-red spots that may develop pale centers or scorched-looking leaves.',
    actions: [
      'Remove badly affected dead leaves and plant debris.',
      'Avoid overcrowding and prolonged leaf wetness.',
      'Confirm the diagnosis and treatment options with a local strawberry grower adviser.'
    ],
    prevention: 'Use healthy planting material and maintain good bed sanitation.'
  },
  {
    match: 'tomato___bacterial_spot',
    name: 'Tomato Bacterial Spot',
    cause: 'A bacterial disease spread by splashing water, infected seed, or transplants.',
    symptoms: 'Small dark leaf spots; fruit may develop raised scabby lesions.',
    actions: [
      'Avoid handling plants when wet and sanitize tools.',
      'Remove badly affected debris and avoid overhead watering where practical.',
      'Use clean seed or transplants and seek locally approved treatment guidance.'
    ],
    prevention: 'Rotate away from susceptible crops and avoid working in wet plants.'
  },
  {
    match: 'tomato___early_blight',
    name: 'Tomato Early Blight',
    cause: 'A fungal disease that commonly affects older leaves, especially under wet conditions.',
    symptoms: 'Brown spots with concentric rings, often starting on lower leaves.',
    actions: [
      'Remove badly affected lower leaves when practical.',
      'Water at the soil level and clean up fallen infected leaves.',
      'Ask a local adviser about tomato-specific registered treatment if symptoms progress.'
    ],
    prevention: 'Use crop rotation, mulch where suitable, and maintain airflow.'
  },
  {
    match: 'tomato___late_blight',
    name: 'Tomato Late Blight',
    cause: 'A rapidly spreading disease favored by humid conditions and leaf wetness.',
    symptoms: 'Irregular water-soaked dark lesions; fruit can also develop firm brown rot.',
    actions: [
      'Seek prompt local agricultural advice if late blight is suspected.',
      'Avoid moving wet suspect foliage between plants.',
      'Follow local guidance for infected material and registered crop protection.'
    ],
    prevention: 'Monitor local disease alerts, use healthy transplants, and reduce prolonged leaf wetness.'
  },
  {
    match: 'tomato___leaf_mold',
    name: 'Tomato Leaf Mold',
    cause: 'A fungal disease favored by high humidity and poor airflow.',
    symptoms: 'Pale yellow patches on upper leaf surfaces and olive-colored growth beneath.',
    actions: [
      'Increase ventilation and spacing where possible.',
      'Avoid wetting foliage and remove severely affected leaves carefully.',
      'For greenhouse crops, ask an adviser about humidity control and suitable registered options.'
    ],
    prevention: 'Reduce persistent humidity and maintain airflow around leaves.'
  },
  {
    match: 'tomato___septoria_leaf_spot',
    name: 'Tomato Septoria Leaf Spot',
    cause: 'A fungal disease that can survive in infected plant debris and spread by splashing water.',
    symptoms: 'Many small circular spots with pale centers and dark edges, often on lower leaves.',
    actions: [
      'Remove badly affected lower leaves when practical.',
      'Clear fallen infected debris and water near the soil.',
      'Ask a local adviser about tomato-specific registered treatment if the disease spreads.'
    ],
    prevention: 'Rotate crops, mulch where suitable, and avoid prolonged leaf wetness.'
  },
  {
    match: 'tomato___spider_mites',
    name: 'Tomato Two-Spotted Spider Mite Damage',
    cause: 'Tiny mites that feed on leaf tissue; hot, dry conditions can favor outbreaks.',
    symptoms: 'Fine pale stippling, bronzing, and sometimes delicate webbing.',
    actions: [
      'Inspect leaf undersides with a magnifier to confirm mites.',
      'Reduce plant stress and manage dust where practical.',
      'Ask a local adviser about suitable registered mite-control options before applying a product.'
    ],
    prevention: 'Monitor leaf undersides and conserve beneficial predatory insects where possible.'
  },
  {
    match: 'tomato___target_spot',
    name: 'Tomato Target Spot',
    cause: 'A fungal disease favored by warm, humid conditions and leaf wetness.',
    symptoms: 'Brown circular lesions that may develop concentric rings.',
    actions: [
      'Remove badly affected leaves and fallen debris where practical.',
      'Improve airflow and water at soil level.',
      'Confirm the disease and treatment choice with a local tomato specialist.'
    ],
    prevention: 'Use crop rotation, suitable spacing, and clean planting material.'
  },
  {
    match: 'tomato___yellow_leaf_curl_virus',
    name: 'Tomato Yellow Leaf Curl Virus',
    cause: 'A viral disease commonly transmitted by whiteflies.',
    symptoms: 'Upward-curling yellow leaves, stunted growth, and poor fruit set.',
    actions: [
      'Inspect plants for whiteflies and seek local confirmation of the virus.',
      'Remove suspect plants only according to local plant-health guidance.',
      'Do not use fungicides to try to cure a viral infection.'
    ],
    prevention: 'Use healthy transplants, resistant varieties where available, and locally recommended whitefly management.'
  },
  {
    match: 'tomato___mosaic_virus',
    name: 'Tomato Mosaic Virus',
    cause: 'A viral disease that can spread through contaminated hands, tools, and plant material.',
    symptoms: 'Mottled light and dark green leaves, distortion, and reduced growth.',
    actions: [
      'Clean hands and tools after handling suspect plants.',
      'Avoid saving seed from suspect plants and seek confirmation if symptoms are unclear.',
      'Follow local guidance on removing infected plants; there is no curative pesticide for the virus.'
    ],
    prevention: 'Use clean seed, sanitize tools, and avoid tobacco contamination when handling plants.'
  }
];

function getGuidance(disease) {
  const key = disease.toLowerCase().replace(/[^a-z0-9]/g, '');
  const specificGuidance =
    diseaseGuidance.find((item) => key.includes(item.match.toLowerCase().replace(/[^a-z0-9]/g, ''))) || null;

  // Use disease-specific content when available; otherwise give cautious general
  // next steps so every model class can still receive a useful result.
  if (specificGuidance) return specificGuidance;

  const readableName = disease
    .replace(/___/g, ' - ')
    .replace(/_/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  return {
    name: readableName || 'Plant disease / condition',
    cause: 'The model predicted this class from the leaf image. The exact cause cannot be confirmed from an image alone.',
    symptoms: 'Compare the leaf with other leaves on the same plant. Check the upper and lower leaf surfaces for spots, yellowing, curling, wilting, powdery growth, or spreading lesions.',
    actions: [
      'Take clear photos of the whole plant and both sides of affected leaves, and compare symptoms across several leaves.',
      'Keep affected plants separate when practical; clean hands and tools after handling them, and remove fallen plant debris.',
      'Avoid applying pesticides until the disease is confirmed. Ask a local agricultural extension officer or plant-health specialist to identify the condition and recommend locally registered treatment.'
    ],
    prevention: 'Use healthy planting material, keep tools clean, provide suitable spacing and airflow, water near the soil where practical, and monitor new growth regularly.'
  };
}

export default function Remedies() {
  const { state: prediction } = useLocation();
  const [showRemedies, setShowRemedies] = React.useState(false);

  const disease =
    typeof prediction?.disease === 'string' && prediction.disease.trim()
      ? prediction.disease.trim()
      : '';

  // Only accept an explicit positive leaf confirmation from the backend.
  const isLeaf =
    prediction?.is_leaf === true ||
    String(prediction?.is_leaf).toLowerCase() === 'true';

  const isHealthy = disease.toLowerCase().includes('healthy');
  const confidenceValue = prediction?.confidence;
  const confidence = Number(confidenceValue);
  const hasConfidence =
    confidenceValue !== null &&
    confidenceValue !== undefined &&
    confidenceValue !== '' &&
    Number.isFinite(confidence);

  const hasDiagnosis = Boolean(
    prediction && isLeaf && disease && disease.toLowerCase() !== 'unknown'
  );

  const plantName = !isLeaf
    ? 'Required: A plant leaf'
    : disease.includes('___')
      ? disease.split('___')[0].replace(/_/g, ' ')
      : 'Plant';

  const backendDetails = prediction?.details;
  const staticGuidance = hasDiagnosis && !isHealthy ? getGuidance(disease) : null;
  const guidance = backendDetails
    ? {
        name: backendDetails.disease_name || formattedDisease,
        cause: backendDetails.causes?.join(' ') || backendDetails.description || '',
        symptoms: backendDetails.symptoms?.join(' ') || '',
        actions: [
          ...(backendDetails.immediate_actions || []),
          ...(backendDetails.organic_treatments || []),
          ...(backendDetails.chemical_treatments || []),
        ],
        prevention: backendDetails.prevention_tips?.join(' ') || '',
      }
    : staticGuidance;
  const formattedDisease = disease
    .replace(/___/g, ' - ')
    .replace(/_/g, ' ') || 'Not identified';

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-white py-10">
      <div className="mx-auto max-w-5xl px-4">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          className="overflow-hidden rounded-3xl bg-white shadow-xl"
        >
          <div className="bg-gradient-to-r from-green-700 to-emerald-500 px-6 py-7 text-white md:px-8">
            <div className="flex items-center gap-3">
              <FaLeaf className="text-3xl" />
              <div>
                <h1 className="text-2xl font-bold md:text-3xl">
                  Plant Care & Disease Guidance
                </h1>
                <p className="mt-1 text-green-50">
                  DeepLeaf plant health analysis
                </p>
              </div>
            </div>
          </div>

          {!prediction ? (
            <div className="p-6 md:p-8">
              <div className="rounded-xl bg-amber-50 p-5 text-amber-900">
                Upload a leaf image and run detection first to view its result and remedies.
              </div>
              <Link
                to="/detection"
                className="mt-5 inline-block rounded-xl bg-green-600 px-5 py-3 font-semibold text-white hover:bg-green-700"
              >
                Go to Detection
              </Link>
            </div>
          ) : !isLeaf ? (
            <div className="p-6 md:p-8">
              <div className="rounded-xl bg-amber-50 p-5 text-amber-900">
                <h2 className="flex items-center gap-2 text-xl font-bold">
                  <FaExclamationTriangle /> Leaf Not Confirmed
                </h2>
                <p className="mt-2"><strong>Required:</strong> A plant leaf</p>
                <p className="mt-2">
                  The image could not be confirmed as a plant leaf. Please upload a clear photo of a plant leaf. Disease-specific treatment is not available for this result.
                </p>
              </div>
            </div>
          ) : !hasDiagnosis ? (
            <div className="p-6 md:p-8">
              <div className="rounded-xl bg-amber-50 p-5 text-amber-900">
                <h2 className="flex items-center gap-2 text-xl font-bold">
                  <FaExclamationTriangle /> Disease Not Confirmed
                </h2>
                <p className="mt-2"><strong>Plant:</strong> {plantName}</p>
                <p className="mt-2">
                  A plant leaf was detected, but the disease could not be identified reliably. Please upload a clear, well-lit image of a supported plant leaf. No disease-specific treatment is recommended until the condition is confirmed.
                </p>
                <p className="mt-3"><strong>Model confidence:</strong> {hasConfidence ? `${confidence.toFixed(2)}%` : 'Not available'}</p>
              </div>
              <Link to="/detection" className="mt-5 inline-block rounded-xl bg-green-600 px-5 py-3 font-semibold text-white hover:bg-green-700">
                Upload Another Image
              </Link>
            </div>
          ) : (
            <div className="p-6 md:p-8">
              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <div className="flex min-h-64 items-center justify-center overflow-hidden rounded-2xl border border-green-100 bg-green-50 p-3">
                  {prediction.preview ? (
                    <img
                      src={prediction.preview}
                      alt="Uploaded leaf used for prediction"
                      className="max-h-80 w-full rounded-xl object-contain"
                    />
                  ) : (
                    <div className="py-10 text-center text-green-800">
                      <FaLeaf className="mx-auto mb-3 text-5xl" />
                      <p className="font-semibold">Leaf image preview unavailable</p>
                      <p className="mt-1 text-sm text-green-700">
                        Run a new detection to include the uploaded image.
                      </p>
                    </div>
                  )}
                </div>

                <div className="flex flex-col justify-center">
                  <div className={`inline-flex w-fit items-center gap-2 rounded-full px-4 py-2 text-sm font-bold ${
                    isHealthy
                      ? 'bg-green-100 text-green-800'
                      : 'bg-amber-100 text-amber-800'
                  }`}>
                    {isHealthy ? <FaCheckCircle /> : <FaExclamationTriangle />}
                    {isHealthy ? 'Healthy prediction' : 'Detected condition'}
                  </div>

                  <h2 className="mt-4 text-2xl font-bold text-gray-900 md:text-3xl">
                    {formattedDisease || 'Unknown condition'}
                  </h2>
                  <p className="mt-2 text-gray-600">
                    <strong>Plant:</strong> {plantName}
                  </p>

                  <div className="mt-6 rounded-2xl bg-gray-50 p-5">
                    <div className="mb-3 flex items-center justify-between gap-3">
                      <span className="font-medium text-gray-700">Model confidence</span>
                      <span className="font-bold text-green-700">
                        {hasConfidence ? `${confidence.toFixed(2)}%` : 'Unavailable'}
                      </span>
                    </div>
                    <div
                      className="h-3 w-full overflow-hidden rounded-full bg-gray-200"
                      role="progressbar"
                      aria-label="Model confidence"
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-valuenow={hasConfidence ? Math.min(100, Math.max(0, confidence)) : 0}
                    >
                      <div
                        className="h-full rounded-full bg-green-500 transition-all"
                        style={{
                          width: `${hasConfidence ? Math.min(100, Math.max(0, confidence)) : 0}%`
                        }}
                      />
                    </div>
                  </div>
                </div>
              </div>

              {isHealthy ? (
                <div className="mt-6 rounded-xl border border-green-200 bg-green-50 p-5 text-green-900">
                  <h3 className="flex items-center gap-2 text-lg font-bold">
                    <FaCheckCircle /> Healthy leaf
                  </h3>
                  <p className="mt-2">
                    No disease treatment is suggested from this prediction. Continue suitable watering,
                    sunlight, and regular monitoring.
                  </p>
                </div>
              ) : (
                <>
                  <div className="mt-6 rounded-2xl border border-red-100 bg-red-50 p-5">
                    <h3 className="text-lg font-bold text-red-800">
                      {guidance?.name || formattedDisease}
                    </h3>
                  </div>

                  <button
                    type="button"
                    onClick={() => setShowRemedies((previous) => !previous)}
                    aria-expanded={showRemedies}
                    className="mt-6 w-full rounded-xl bg-green-600 px-5 py-3 font-semibold text-white transition hover:bg-green-700"
                  >
                    {showRemedies ? 'Hide Remedies ▲' : 'View Remedies & Treatment ▼'}
                  </button>

                  {showRemedies && guidance && (
                    <div className="mt-6 space-y-5 rounded-2xl border border-green-100 bg-white p-5 md:p-6">
                      <section>
                        <h3 className="text-lg font-bold text-gray-900">Possible cause</h3>
                        <p className="mt-1 text-gray-700">{guidance.cause}</p>
                      </section>

                      <section>
                        <h3 className="text-lg font-bold text-gray-900">Symptoms to check</h3>
                        <p className="mt-1 text-gray-700">{guidance.symptoms}</p>
                      </section>

                      <section>
                        <h3 className="text-lg font-bold text-gray-900">Disease management</h3>
                        <ul className="mt-2 space-y-3">
                          {guidance.actions.map((action, index) => (
                            <li key={index} className="flex gap-3 text-gray-700">
                              <FaLeaf className="mt-1 shrink-0 text-green-600" />
                              <span>{action}</span>
                            </li>
                          ))}
                        </ul>
                      </section>

                      <section>
                        <h3 className="text-lg font-bold text-gray-900">Prevention</h3>
                        <p className="mt-1 text-gray-700">{guidance.prevention}</p>
                      </section>

                    </div>
                  )}
                </>
              )}

              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <Link
                  to="/detection"
                  className="flex-1 rounded-xl bg-green-600 px-6 py-3 text-center font-semibold text-white transition hover:bg-green-700"
                >
                  New Detection
                </Link>
                <Link
                  to="/result"
                  state={prediction}
                  className="flex-1 rounded-xl border-2 border-green-600 px-6 py-3 text-center font-semibold text-green-700 transition hover:bg-green-50"
                >
                  Back to Prediction Result
                </Link>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}

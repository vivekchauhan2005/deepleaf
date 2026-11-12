
const API_URL = 'http://127.0.0.1:8002';

const emptyComparison = {
  cnn: { disease: null, confidence: null },
  vgg19: { disease: null, confidence: null },
};

const emptyEvidence = {
  available: false,
  plant: null,
  disease: null,
  images: [],
};

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');

  if (!token) {
    throw new Error('Please log in before making a prediction.');
  }

  return {
    Authorization: `Bearer ${token}`,
  };
};

export const predictDisease = async (imageFile) => {
  if (!imageFile) {
    throw new Error('Please select an image file.');
  }

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];

  if (!allowedTypes.includes(imageFile.type)) {
    throw new Error('Please upload a JPG, PNG, or WEBP image.');
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  let response;

  try {
    response = await fetch(`${API_URL}/predict/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        'Cannot connect to the DeepLeaf backend. Make sure it is running on port 8002.'
      );
    }
    throw error;
  }

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error('The backend returned an invalid response.');
  }

  if (response.status === 401) {
    throw new Error('Your login session is invalid or expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(
      typeof data?.detail === 'string' ? data.detail : 'Prediction failed.'
    );
  }

  if (data?.success !== true) {
    throw new Error(data?.message || 'The prediction could not be completed.');
  }

  if (typeof data.is_leaf !== 'boolean') {
    throw new Error('The backend did not confirm whether this image contains a leaf.');
  }

  const leafConfidence =
    data.leaf_confidence !== null &&
    data.leaf_confidence !== undefined &&
    data.leaf_confidence !== '' &&
    Number.isFinite(Number(data.leaf_confidence))
      ? Number(data.leaf_confidence)
      : null;

  const common = {
    success: true,
    leaf_confidence: leafConfidence,
    filename: data.filename || imageFile.name,
    dataset_evidence: data.dataset_evidence || emptyEvidence,
    comparison: data.comparison || emptyComparison,
    candidates_comparison: Array.isArray(data.candidates_comparison) ? data.candidates_comparison : [],
    comparison_graph_base64: data.comparison_graph_base64 || null,
    comparison_graph_url: data.comparison_graph_url || null,
    record_id: data.record_id || null,
    history_saved: data.history_saved === true,
    details: data.details || null,
    top_predictions: data.top_predictions || [],
    formatted_disease: data.formatted_disease || null,
    plant_name: data.plant_name || null,
    severity: data.severity || null,
    status: data.status || null,
    models_agree: data.models_agree || false,
    species_agree: data.species_agree || false,
    photography_tips: data.photography_tips || [],
    supported_crops: data.supported_crops || [],
    herb_guide: data.herb_guide || null,
    unsupported_species_note: data.unsupported_species_note || null,
  };

  if (data.is_leaf === false) {
    return {
      ...common,
      is_leaf: false,
      disease: null,
      confidence: null,
      message:
        data.message ||
        'No plant leaf was detected. Please upload a clear image of a plant leaf.',
    };
  }

  const disease =
    typeof data.disease === 'string' && data.disease.trim()
      ? data.disease.trim()
      : null;

  const confidence =
    data.confidence !== null &&
    data.confidence !== undefined &&
    data.confidence !== '' &&
    Number.isFinite(Number(data.confidence))
      ? Number(data.confidence)
      : null;

  return {
    ...common,
    is_leaf: true,
    disease,
    confidence,
    message: data.message || 'Disease classification completed.',
  };
};

export const checkBackendHealth = async () => {
  let response;

  try {
    response = await fetch(`${API_URL}/health`);
  } catch {
    throw new Error('Cannot connect to the DeepLeaf backend on port 8002.');
  }

  if (!response.ok) {
    throw new Error('The DeepLeaf backend health check failed.');
  }

  return response.json();
};

export default API_URL;

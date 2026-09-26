const API_URL = 'http://127.0.0.1:8000';

export const predictDisease = async (imageFile) => {
  if (!imageFile) {
    throw new Error('Please select an image');
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(`${API_URL}/predict/`, {
    method: 'POST',
    body: formData,
  });

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error('Invalid response from server');
  }

  if (!response.ok) {
    throw new Error(
      data?.detail || 'Prediction failed'
    );
  }

  if (!data.success) {
    throw new Error(
      data?.message || 'Prediction was not successful'
    );
  }

  const confidence = Number(data.confidence ?? 0);

  const isLeaf = data.is_leaf !== false;

  if (!isLeaf) {
    return {
      success: true,
      is_leaf: false,
      filename: data.filename,
      disease: null,
      confidence: 0,
      message:
        data.message ||
        'Please enter a plant leaf image.',
      dataset_evidence: null,
      comparison: {
        cnn: {
          disease: null,
          confidence: null,
        },
        vgg19: {
          disease: null,
          confidence: null,
        },
      },
    };
  }

  return {
    success: true,
    is_leaf: true,
    filename: data.filename,

    disease:
      data.disease || null,

    confidence:
      confidence,

    message:
      data.message ||
      'Disease identified successfully.',

    dataset_evidence:
      data.dataset_evidence || {
        available: false,
        plant: null,
        disease: null,
        images: [],
      },

    comparison:
      data.comparison || {
        cnn: {
          disease: null,
          confidence: null,
        },
        vgg19: {
          disease: null,
          confidence: null,
        },
      },
  };
};

export const checkBackendHealth = async () => {
  const response = await fetch(
    `${API_URL}/health`
  );

  if (!response.ok) {
    throw new Error(
      'Backend server is not running'
    );
  }

  return await response.json();
};

export default API_URL;
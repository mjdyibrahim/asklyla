export const getUserAccount = async () => {
  try {
    const response = await fetch('/api/account', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user account:', error);
    throw error;
  }
}

export const getUserSettings = async () => {
  try {
    const response = await fetch('/api/settings', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user settings:', error);
    throw error;
  }
}
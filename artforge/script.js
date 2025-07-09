// I define the correct endpoint of my deployed API Gateway
const API_URL = "https://jvijvw9pmj.execute-api.us-west-2.amazonaws.com/prod/generate-image";

async function generateImage() {
  // I get the prompt value entered by the user
  const prompt = document.getElementById("promptInput").value;

  // I target the status area and image container in the HTML
  const status = document.getElementById("status");
  const imageContainer = document.getElementById("imageContainer");

  // I reset the UI before sending the request
  status.textContent = "🧠 Generating image...";
  imageContainer.innerHTML = "";

  try {
    // I send the prompt to my Lambda API using a POST request
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    // I check if the response is OK
    if (!response.ok) {
      throw new Error("API error");
    }

    const data = await response.json();

    // I check if the image URL is present in the response
    if (data.image_url) {
      // I create an <img> element and set its source to the generated image
      const img = document.createElement("img");
      img.src = data.image_url;
      img.alt = "Generated image";

      // I insert the image into the container and update the status
      imageContainer.appendChild(img);
      status.textContent = "✅ Image generated successfully!";
    } else {
      throw new Error("Missing image_url in response");
    }

  } catch (error) {
    // I handle any errors and update the UI accordingly
    console.error("Image generation failed:", error);
    status.textContent = "❌ Failed to generate image. Try again.";
  }
}

// I reset the input, image, and status
function clearImage() {
  document.getElementById("promptInput").value = "";
  document.getElementById("imageContainer").innerHTML = "";
  document.getElementById("status").textContent = "";
}

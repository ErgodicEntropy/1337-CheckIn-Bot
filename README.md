# 1337-CheckIn-Bot
If everyone has a gun, the gun loses its comparative advantage: mutually-assured destruction pushes equal and contending powers towards homeostasis.

# Purpose
As the description briefly puts it, the point of open-sourcing (and reiterating) the code of check-in bots is to proliferate them as much as possible. This stems from few observations that I had (which are partially inspired by mechanism design, behavioral economics and game theory):

1. Comparative advantage doesn't scale: this observation is in complete contrast to Metcalfe's law but it goes as follow: the more user nodes are added into the bot usage network, the less comparatively effective bot usage becomes (though competitive advantage is potentially intact due to differentiation, but again, the point of the project is to initiate a strategic orientation and proliferate at least a mental model for the layman)
2. Equal contending powers are stable if sufficient deterrence mechanism is at place: second-strike capability, even if merely estimated by a node on other nodes, effectively nullifies the incentives to use check-in bots given actual or merely perceived total uniformity of competitive advantage. The ambiguity effect gridlocks subjective expected-utility action.
3. Total uniformity of competitive advantage can only be maximal: To make point 2 possible, competitive advantage should be uniformly distributed. The only way where this is possible is if everybody is using the same allele variant of the tech (centralization), but the incentives to use the same allele variant of the tech is predicated on the plausibility that the allele variant in question is the most evolutionarily adaptive (maximum fitness or efficiency) or, again, perceived to be as such (it should be fairly obvious that actual fitness is asymptocally stable whereas perceived fitness is merely simply stable). This is just the asymmetry of incentives at play i.e., small and specialized interest groups consistently overpower the large and unorganized majority because it's easy to uniformize a competitive advantage in the former than in the latter. This happens by concentrating all benefits and dispersing the costs due to the tragedy of the commons (check-in being a shared resource which is also rival and non-excludable). 


These 3 points offer a political-economy solution to a technical problem. As such, they're a mere workaround but still a worthy attempt in my view. The answer to whether the current state of things is unconditionally effective or not is a resounding no. By no means this is a fully-robust immunological solution. Reiteration is needed.

# How to Use

## 1. Clone or Download the Project

Clone the repository using Git:

```bash
git clone <repository_url>
cd <project_folder>
```

Or download the ZIP file manually and extract it.

---

## 2. Install Python Requirements

Make sure you have Python installed on your machine.

- Recommended Python version: **Python 3.10+**
- Verify installation:

```bash
python --version
```

Install all required dependencies:

```bash
pip install -r requirements.txt
```

If you are using multiple Python versions, you may need:

```bash
pip3 install -r requirements.txt
```

### Optional: Create a Virtual Environment

Using a virtual environment is recommended to avoid dependency conflicts.

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install requirements again inside the environment:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Your Credentials

Open the main script or configuration file and insert your account credentials.

Example:

```python
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
```

Replace the placeholders with your actual credentials.

> Keep your credentials private and never share them publicly or upload them to GitHub.

---

## 4. Configure Discord Webhook (Optional)

Discord webhooks allow the application to send notifications directly to a Discord channel.

### Step-by-Step Discord Webhook Setup

#### Create a Discord Server (Skip if You Already Have One)

- Open Discord
- Click the **"+"** button on the left sidebar
- Select:
  - **Create My Own**
  - Choose:
    - For me and my friends
    - Or for a community
- Enter a server name
- Click **Create**

---

#### Create or Select a Channel

- Inside your server:
  - Click the **"+"** next to **Text Channels**
  - Create a new channel
  - Example:
    - `notifications`
    - `logs`
    - `alerts`

Or use an existing channel.

---

#### Enable Webhooks

- Hover over the target channel
- Click the **gear icon** (Edit Channel)
- In the left sidebar:
  - Select **Integrations**
- Click:
  - **Webhooks**
- Press:
  - **New Webhook**

---

#### Configure the Webhook

You can customize:

- Webhook name
  - Example:
    - `Ticket Monitor`
    - `Bot Alerts`
- Webhook avatar (optional)

Make sure the webhook is assigned to the correct channel.

---

#### Copy the Webhook URL

- Click:
  - **Copy Webhook URL**

It should look similar to:

```text
https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz
```

---

#### Insert the Webhook URL Into the Project

Paste the URL into the appropriate variable in the script or configuration file.

Example:

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_here"
```

If you do not want Discord notifications, you can leave this field empty.

---

## 5. Run the Project

Start the application using:

```bash
python main.py
```

Or depending on the filename:

```bash
python app.py
```

---

# Common Issues

## `ModuleNotFoundError`

Install missing dependencies again:

```bash
pip install -r requirements.txt
```

---

## Python Not Found

Ensure Python is installed and added to PATH.

Test with:

```bash
python --version
```

---

## Discord Webhook Not Sending Messages

Check that:

- The webhook URL is correct
- The webhook was not deleted
- The channel permissions allow webhooks
- Internet connection is active

---

## Invalid Login or Authentication Errors

Verify that:

- Email and password are correct
- The account is accessible normally through the website
- Any required verification steps are completed

---

# Security Recommendations

- Never hardcode sensitive credentials in public repositories
- Use environment variables when possible
- Do not share your Discord webhook publicly
  - Anyone with the webhook URL can send messages to your channel

Example using environment variables:

```python
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
```

Example `.env` file:

```env
EMAIL=your_email@example.com
PASSWORD=your_password
WEBHOOK_URL=https://discord.com/api/webhooks/...
```

---

# Notes

- Ensure your internet connection is stable while running the application
- Some features may require updated browser drivers or dependencies
- Running inside a virtual environment is strongly recommended for stability



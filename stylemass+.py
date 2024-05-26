import os
import replicate
import requests
import random
import re

# Load prompts from individual files
def load_prompts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

# Get a valid prompt file number
def get_valid_prompt_file_number(prompt_dir):
    prompt_files = os.listdir(prompt_dir)
    return random.choice(prompt_files)

# Set up directories
text_data_dir = "prompts"
os.makedirs(text_data_dir, exist_ok=True)
output_dir = os.path.join("OUTPUTS", "MERGEME")
os.makedirs(output_dir, exist_ok=True)
output_urls_file = os.path.join(text_data_dir, "completed_image_urls.txt")

# Set API token
os.environ["REPLICATE_API_TOKEN"] = "r8_US201XL5poq7vjpzqR8BcKhMX8pUYZS3npIMJ"
client = replicate.Client()

# List of artists and modifiers
artists = [
"Takashi Murakami", "Beeple", "Tyler Edlin", "Andrew Robinson", "Anton Fadeev", "Chris Labrooy", "Dan Mumford", "Michelangelo", "Noah Bradley", "Cassius Marcellus Coolidge", "Ted Nasmith", "James Gurney", "James Paick", "Justin Gerard", "Jakub Różalski", "Jeff Easley", "Agnes Lawrence Pelton", "Alan Lee", "Bob Byerley", "Bob Eggleton", "Chris Foss", "Chris Moore", "Eiichiro Oda", "Jeremey Smith", "Jeremiah Ketner", "Michael Whelan", "Mike Winkelmann", "JR", "Banksy", "Shepard Fairey", "Yayoi Kusama", "David LaChapelle", "Cindy Sherman", "Ai Weiwei", "Marina Abramović", "Annie Leibovitz", "Nan Goldin", "Damien Hirst", "Tracey Emin", "Olafur Eliasson", "Kehinde Wiley", "Yinka Shonibare", "Grayson Perry", "Wolfgang Tillmans", "Jeff Koons", "David Hockney", "Kara Walker", "Hiroshi Sugimoto", "Anish Kapoor", "Julie Mehretu", "Peter Doig", "Wolfgang Laib", "Shirin Neshat", "Kerry James Marshall", "Mark Bradford", "Cai Guo-Qiang", "Cornelia Parker", "Carrie Mae Weems", "Gerhard Richter", "Matthew Barney", "Sarah Sze", "Chris Ofili", "Thomas Ruff", "Jenny Saville", "Elizabeth Peyton", "Glenn Ligon", "Mariko Mori", "Antony Gormley", "Tom Friedman", "Trenton Doyle Hancock", "Do Ho Suh", "Paula Rego", "Rachel Whiteread", "Huma Bhabha", "George Condo", "Ron Mueck", "John Currin", "Elizabeth Murray", "Rudolf Stingel", "Kara Walker", "Tom Friedman", "Fred Tomaselli", "Luc Tuymans", "Katharina Grosse", "Julian Schnabel", "Cindy Sherman", "Thomas Struth", "Philip-Lorca diCorcia", "Andreas Gursky", "Thomas Demand", "Thomas Ruff", "Hiroshi Sugimoto", "Marlene Dumas", "Bruce Nauman", "John Baldessari", "Ed Ruscha", "Yinka Shonibare", "Chris Ofili", "Gilbert & George", "Jeff Wall", "Nam June Paik", "Matthew Barney", "Paul McCarthy", "Yayoi Kusama", "Cao Fei", "Olafur Eliasson", "Bill Viola", "Doug Aitken", "Pipilotti Rist", "James Turrell", "Richard Serra", "Dan Flavin", "Rachel Whiteread", "Kara Walker", "Carrie Mae Weems", "Marina Abramović", "Louise Bourgeois", "Mona Hatoum", "Anish Kapoor", "Damien Hirst", "Ai Weiwei", "Yoko Ono", "Christian Boltanski", "Jenny Holzer", "Barbara Kruger", "Cindy Sherman", "Marilyn Minter", "Wangechi Mutu", "Catherine Opie", "Shirin Neshat", "Tracey Emin", "Kiki Smith", "Francesca Woodman", "Sophie Calle", "Nan Goldin", "Roni Horn", "Nancy Spero", "Patty Chang", "Shirin Neshat", "Adrian Piper", "Kara Walker", "Cindy Sherman", "Nan Goldin", "Carrie Mae Weems", "Mona Hatoum", "Lorna Simpson", "Roni Horn", "Shirin Neshat", "Dana Schutz", "Sarah Sze", "Catherine Opie", "Jenny Saville", "Mickalene Thomas", "Julie Mehretu", "Wangechi Mutu", "Kara Walker", "Yinka Shonibare", "Chris Ofili", "Steve McQueen", "Kehinde Wiley", "Glenn Ligon", "Lorna Simpson", "Kara Walker", "Njideka Akunyili Crosby", "Toyin Ojih Odutola", "Kerry James Marshall", "Mark Bradford", "Rashid Johnson", "Julie Mehretu", "Theaster Gates", "Titus Kaphar", "Nina Chanel Abney", "Njideka Akunyili Crosby", "Amy Sherald", "Jordan Casteel", "Adrian Ghenie", "George Condo", "Kehinde Wiley", "Yayoi Kusama", "Rudolf Stingel", "Damien Hirst", "Jeff Koons", "Takashi Murakami", "Kara Walker", "Banksy", "Yinka Shonibare", "Ai Weiwei", "Cindy Sherman", "Marina Abramović", "Tracey Emin", "Olafur Eliasson", "Gerhard Richter", "Matthew Barney", "Hans Haacke", "Anish Kapoor", "Barbara Kruger", "Maurizio Cattelan", "Chris Ofili", "Gilbert & George", "Shirin Neshat", "Antony Gormley", "Do Ho Suh", "Marlene Dumas", "Bruce Nauman", "John Baldessari", "Ed Ruscha", "Chris Burden", "Nam June Paik", "Louise Bourgeois", "Damien Hirst", "Takashi Murakami", "JR", "Banksy", "Shepard Fairey", "Yayoi Kusama", "David LaChapelle", "Cindy Sherman", "Ai Weiwei", "Marina Abramović", "Annie Leibovitz", "Nan Goldin"
]

modifiers = [
    '4K', 'unreal engine', 'octane render', '8k octane render', 'photorealistic', 'mandelbulb fractal', 
    'Highly detailed carvings', 'Atmosphere', 'Dramatic lighting', 'Sakura blossoms', 'magical atmosphere', 
    'muted colors', 'Highly detailed', 'Epic composition', 'incomparable reality', 'ultra detailed', 
    'unreal 5', 'concept art', 'smooth', 'sharp focus', 'illustration, evocative', 'mysterious', 'epic scene', 
    'intricate details', 'Pop Surrealism', 'sharp photography', 'hyper realistic', 'maximum detail', 'ray tracing', 
    'volumetric lighting', 'photorealistic', 'cinematic', 'realistic lighting', 'high resolution render', 'hyper realism', 
    'insanely detailed', 'intricate', 'volumetric light', 'light rays', 'shock art', 'dystopian art', 'cgsociety', 
    'fantasy art', 'matte drawing', 'speed painting', 'darksynth', 'redshift', 'color field', 'rendered in cinema4d', 
    'imax', '#vfxfriday', 'hyper realism', 'oil on canvas', 'figurative art', 'detailed painting', 'soft mist', 'daz3d', 
    'zbrush', 'anime', 'behance hd', 'panfuturism', 'futuristic', 'pixiv', 'auto-destructive art', 'apocalypse art', 
    'afrofuturism', 'reimagined by industrial light and magic', 'metaphysical painting', 'wiccan', 'grotesque', 'whimsical', 
    'psychedelic art', 'digital art', 'fractalism', 'panfuturism', 'anime aesthetic', 'chiaroscuro', 'mystical', 'majestic', 
    'digital painting', 'psychedelic', 'synthwave', 'cosmic horror', 'lovecraftian', 'vanitas', 'apocalypse art', 'macabre', 
    'toonami', 'hologram', 'magic realism', 'impressionism', 'neo-fauvism', 'fauvism', 'synchromism', 'darksynth', 'fractalism', 'redshift'
]

# Generate a random prompt with artists and modifiers
def generate_random_prompt(prompt, artist1, artist2, modifier1, modifier2, randomized):
    return f"{artist1} & {artist2}, {modifier1}, {modifier2}, {prompt}"

# Number of iterations
num_iterations = 30

# Validate URL
def validate_url(url):
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Get a valid image URL
def get_valid_image_url(base_url, start, end, extension="jpg"):
    for _ in range(10): 
        image_number = random.randint(start, end)
        image_url = f"{base_url}{image_number}.{extension}"
        print(f"Generated image URL: {image_url}")
        if validate_url(image_url):
            print("Valid image URL found.")
            return image_url
        else:
            print("Invalid image URL.")
    return None

# Get the last processed image number
def get_last_image_number(output_dir):
    try:
        with open(output_urls_file, "r") as f:
            last_image_url = f.readlines()[-1].strip()
            last_image_number = int(re.findall(r'\d+', last_image_url.split("/")[-1])[0])
        return last_image_number
    except (IndexError, FileNotFoundError):
        return 0

# Run style transfer
def run_style_transfer(idx, structure_image_url, style_image_url, prompt, denoise_strength, output_dir):
    print(f"Starting style transfer for image {idx} with denoise strength {denoise_strength}")
    try:
        output = replicate.run(
            "fofr/style-transfer:f1023890703bc0a5a3a2c21b5e498833be5f6ef6e70e9daf6b9b3a4fd8309cf0",
            {
                "style_image": style_image_url,
                "structure_image": structure_image_url,
                "model": "high-quality",
                "width": 1024,
                "height": 1024,
                "prompt": prompt,
                "output_format": "png",
                "output_quality": 100,
                "negative_prompt": "bird, feathers, female, woman, dress, face, eyes, animal, man, human, hands, eyes, face, mouth, nose, human, man, woman, animal, hair, cloth, sheets",
                "number_of_images": 1,
                "structure_depth_strength": 1.2,
                "structure_denoising_strength": denoise_strength
            }
        )
        process_output(output, idx, output_dir)
    except Exception as e:
        print(f"Failed style transfer for image {idx}: {e}")

# Process output
def process_output(output, idx, output_dir):
    print(f"Processing output for image {idx}")
    if isinstance(output, list) and len(output) > 0:
        transformed_image_url = output[0]
        try:
            transformed_img_response = requests.get(transformed_image_url, timeout=10)
            if transformed_img_response.status_code == 200:
                transformed_img_filename = os.path.join(output_dir, f"{idx}.png")
                with open(transformed_img_filename, 'wb') as f:
                    f.write(transformed_img_response.content)
                with open(output_urls_file, "a") as f:
                    f.write(f"{transformed_image_url}\n")
            else:
                print(f"Failed to download styled image {idx}: HTTP {transformed_img_response.status_code}")
        except requests.Timeout:
            print(f"Timeout occurred while downloading styled image {idx}")

# Base image URL
base_image_url = "https://raw.githubusercontent.com/downlifted/aiart/main/stripe/"
newstyle_base_url = "https://raw.githubusercontent.com/downlifted/aiart/main/newnew/"

last_image_number = get_last_image_number(output_dir)

for idx in range(last_image_number + 1, last_image_number + num_iterations + 1):
    try:
        structure_image_url = get_valid_image_url(base_image_url, 1, 40)
        style_image_number = random.randint(1, 217)
        style_image_url = f"{newstyle_base_url}{style_image_number}.jpg"
        prompt_filename = get_valid_prompt_file_number(text_data_dir)
        prompt_file_path = os.path.join(text_data_dir, prompt_filename)
        if os.path.exists(prompt_file_path):
            prompt = load_prompts(prompt_file_path)[0]
            artist1 = random.choice(artists)
            artist2 = random.choice(artists)
            modifier1 = random.choice(modifiers)
            modifier2 = random.choice(modifiers)
            randomized = random.choices([True, False], weights=[0.70, 0.30], k=1)[0]
            if randomized:
                prompt = generate_random_prompt(prompt, artist1, artist2, modifier1, modifier2, randomized)
            print(f"Processing image {idx} with structure URL {structure_image_url} and style URL {style_image_url}")
            print(f"Prompt: {prompt}, from {prompt_file_path}")
            run_style_transfer(idx, structure_image_url, style_image_url, prompt, 0.64, output_dir)
        else:
            print(f"Prompt file {prompt_file_path} not found for image {idx}")
    except Exception as e:
        print(f"Error processing image {idx}: {e}")

from mangum import Mangum
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from enigma.machine import Enigma

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

handler = Mangum(app)

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def encode(
        request: Request,
        plaintext: str = Form(...),

        # Rotor selection
        left_rotor: str = Form(...),
        center_rotor: str = Form(...),
        right_rotor: str = Form(...),

        # Initial rotor positions
        left_initial_position: str = Form(...),
        center_initial_position: str = Form(...),
        right_initial_position: str = Form(...),

        # Ring settings
        left_ring_setting: str = Form(...),
        center_ring_setting: str = Form(...),
        right_ring_setting: str = Form(...),

        # Reflector
        reflector: str = Form(...),

        # Plugboard settings
        plugboard_connections: str = Form("")
):

    try:

        rotors = [left_rotor, center_rotor, right_rotor]
        initial_positions = [x.lower() for x in (left_initial_position, center_initial_position, right_initial_position)]
        ring_settings = [x.lower() for x in (left_ring_setting, center_ring_setting, right_ring_setting)]

        enigma = Enigma(
            rotors=rotors,
            initial_positions=initial_positions,
            ring_settings=ring_settings,
            reflector=reflector,
            plugboard_connections=plugboard_connections,
        )

        # Encrypt the provided plaintext
        ciphertext = enigma.process(plaintext)
        # ciphertext = plaintext

        # Render the template with results
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "plaintext": plaintext,
                "ciphertext": ciphertext,
                "left_rotor": left_rotor,
                "center_rotor": center_rotor,
                "right_rotor": right_rotor,
                "left_initial_position": left_initial_position,
                "center_initial_position": center_initial_position,
                "right_initial_position": right_initial_position,
                "left_ring_setting": left_ring_setting,
                "center_ring_setting": center_ring_setting,
                "right_ring_setting": right_ring_setting,
                "reflector": reflector,
                "plugboard_connections": plugboard_connections,
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e),
                "plaintext": plaintext,
                "ciphertext": "",
                "left_rotor": left_rotor,
                "center_rotor": center_rotor,
                "right_rotor": right_rotor,
                "left_initial_position": left_initial_position,
                "center_initial_position": center_initial_position,
                "right_initial_position": right_initial_position,
                "left_ring_setting": left_ring_setting,
                "center_ring_setting": center_ring_setting,
                "right_ring_setting": right_ring_setting,
                "reflector": reflector,
                "plugboard_connections": plugboard_connections,
            }
        )
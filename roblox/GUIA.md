# Guía: jugar el proyecto en tu PC

Esta guía va desde cero hasta jugar solo en Roblox Studio, jugar con un amigo y publicar el juego.
Los detalles técnicos están en [`README.md`](README.md).

## 1. Qué vas a tener al final

- **Un prototipo jugable**: un mapa de pruebas con combate (puñetazo, combo, patada, espada, bloqueo y parry),
  KOs y sets a 5 contra tu amigo, tablón de récords, un banco que te lanza a la piscina, una carrera de escalada,
  un muñeco de entrenamiento, emotes y el choca esos cinco.
- **27 animaciones R15 propias**, que sustituyen a las de Roblox (andar, correr, saltar, nadar, trepar, sentarse…).
- **Probado en Roblox Studio de verdad**: un plugin de pruebas abre el juego en Studio, juega solo
  (y con 2 jugadores simulados) usando las mismas acciones que tus teclas, el mando o los botones táctiles, y comprueba daño, animaciones, récords,
  KOs, sets y demás. Los resultados están en la sección 9. Aun así, si ves algo raro en *Output*, la
  sección 8 explica qué hacer.

## 2. Qué necesitas instalar

| Herramienta | Para qué | Cómo conseguirla |
|---|---|---|
| **Roblox Studio** | Abrir y probar el juego | Desde create.roblox.com, con tu cuenta de Roblox |
| **Git** | Descargar el proyecto | git-scm.com (en Windows, "Git for Windows") |
| **Rokit** | Instala Rojo y las demás herramientas con las versiones exactas del proyecto | Ver abajo |
| **Python 3** (opcional) | Las comprobaciones y las pruebas automáticas | python.org |

**Herramientas con Rokit (recomendado):** descarga Rokit desde
[github.com/rojo-rbx/rokit/releases](https://github.com/rojo-rbx/rokit/releases) (en Windows,
`rokit-…-windows-x86_64.zip`), descomprímelo y ejecuta `rokit self-install`. Cierra y abre la consola y, en
la carpeta del proyecto, ejecuta:

```bash
rokit install
```

Eso instala lo que pide `rokit.toml`: **Rojo 7.7.1**, **luau-lsp** (comprobación de tipos), **selene**
(linter) y **Lune**. El plugin de Rojo para Studio se instala con `rojo plugin install`.

**Alternativa:** la extensión **Rojo** (de evaera) para Visual Studio Code instala `rojo` y el plugin, y
te deja iniciar el servidor con un clic.

> En este PC ya está todo instalado: Rokit con sus herramientas, Roblox Studio y el plugin de pruebas.

En macOS los pasos son los mismos. Los comandos se escriben en *Terminal* en lugar de *PowerShell*.

## 3. Descargar el proyecto

En PowerShell (Windows) o Terminal (Mac):

```bash
git clone https://github.com/AxxturelHyphen/file_sorter.git
cd file_sorter
```

(El PR ya está fusionado: la rama `master` lo tiene todo. Si ya tienes el repositorio, basta con `git pull`.)

Las carpetas que importan:
- `default.project.json`: le dice a Rojo dónde va cada cosa dentro de Studio.
- `roblox/src/`: el código del juego (Luau).
- `output/rbxmx/`: las 27 animaciones, como KeyframeSequences.

## 4. Abrir el juego en Studio

### Opción rápida: abrir el archivo del juego (sin servidor)

```bash
rojo build -o build/AnimationForge.rbxl
```

Haz doble clic en `build/AnimationForge.rbxl` (o, en Studio, *File → Open from File*). Ya trae el suelo,
el agua de la piscina, el chat nuevo (TextChatService) y personajes R15. Pulsa **Play** y listo.
Lo malo: si cambias el código, tienes que volver a ejecutar `rojo build` y abrirlo otra vez.

### Opción para editar: conectar Studio con Rojo (cambios en vivo)

1. En la carpeta `file_sorter`, inicia el servidor:
   ```bash
   rojo serve
   ```
   Debería decir que escucha en el puerto **34872**. Con VS Code: abre la carpeta, pulsa en *Rojo* en la
   barra inferior y elige `default.project.json`.
2. Abre **Roblox Studio** y crea un lugar nuevo con la plantilla **Baseplate**.
3. En la pestaña *Plugins*, abre **Rojo** y pulsa **Connect**.
4. En el *Explorer* deberías ver:
   - `ReplicatedStorage` → `AnimationPack`, con los módulos, `KeyframeSequences` (27 animaciones) y `Remotes`
   - `ServerScriptService` → `AnimationPackServer` (CombatServer, GameState, Social, TestArena)
   - `StarterPlayer` → `StarterCharacterScripts` → `Animate`
   - `StarterPlayer` → `StarterPlayerScripts` → `CombatInput`, `FeedbackClient`, `AnimationReplicator`
   - `StarterPack` → `Sword`

Mientras `rojo serve` siga abierto, cualquier cambio que guardes en los archivos aparece al instante en Studio.

## 5. Configurar el lugar (una vez)

- **Personajes R15:** en los ajustes del juego (*Game Settings*), sección *Avatar*, elige **R15**. Las
  animaciones solo encajan en personajes R15. Con R6 no se verán bien. Si no puedes cambiar los ajustes porque
  el lugar aún no está publicado, publícalo primero en privado (sección 7).
- **Guarda el lugar** (*File → Save to File* o *Publish*), para no repetir la conexión cada vez.

## 6. Jugar solo

Pulsa **Play**. En Studio, las animaciones se cargan directamente desde las KeyframeSequences sincronizadas,
así que **no hace falta publicar nada para probar solo**.

**El mapa.** Apareces en el centro, mirando al muñeco:
- **Delante:** el **muñeco de entrenamiento** (*Training Dummy*, con barra de vida), con una plataforma
  naranja delante para el reto de daño. A los lados están los carteles de **CONTROLS** (izquierda) y
  **RECORDS** (derecha).
- **A la derecha:** la **torre** (truss) para trepar, con una plataforma verde abajo (salida de la carrera)
  y una campana dorada arriba (meta).
- **A la izquierda:** el **banco** que mira a la piscina, con una palanca roja al lado.
- **Detrás:** la **piscina**, a unos 40 studs.

**Controles y qué deberías ver:**

| Acción | Teclado (mando) | Qué deberías ver |
|---|---|---|
| Moverse / saltar | WASD / Espacio (stick / A) | Animaciones propias de andar o correr. Al caer desde 18+ studs (desde la torre): **aterrizaje de superhéroe**, con polvo y un golpe sordo |
| Agacharse | C o Ctrl izquierdo (B) | Pose de sigilo, andar lento. Golpear a alguien **por la espalda** agachado hace **SNEAK ATTACK x2** |
| Puñetazo / combo | Clic / clic otra vez rápido (R2) | Flash, número de daño, parón breve (hit-stop). El 3.er golpe del combo es **GUARD BREAK** y atraviesa el bloqueo |
| Patada | Q (X) | Manda volando al objetivo, por ejemplo desde la torre o a la piscina ("dunked") |
| Bloquear / parry | Mantener F / pulsar F justo antes del golpe (L2) | "BLOCKED" con clang. Si lo pulsas justo a tiempo: **PARRY!**, y el atacante se tambalea |
| Espada | 1, luego clic | Tajo diagonal con lunge, 22 de daño |
| Emotes | Chat: `/e wave`, `dance`, `cheer`, `point`, `laugh`, `clap`, `salute` | El emote. Si escribes uno que no existe, el chat te da la lista |
| Banco lanzador | Siéntate en el banco; tú u otro jugador pulsáis **E** en la palanca ("Launch!") | Vuelas en arco a la piscina, con una altura distinta cada vez, y una salpicadura que puede batir el récord |
| Carrera de escalada | Pisa la plataforma verde, trepa y toca la campana | Tu tiempo, y "NEW RECORD!" si lo bates |
| Reto del muñeco | **E** en la plataforma naranja ("10 s damage challenge") | Cuenta atrás de 10 s; al final, tu daño total y el récord |

**En móvil o tablet** salen botones en pantalla encima del de saltar: **Hit**, **Kick**, **Block** y
**Crouch**. Los emotes se escriben en el chat igual que en PC. **Con mando** valen los botones entre
paréntesis de la tabla.

**Prueba rápida (5 minutos):**
1. Pega al muñeco: ¿salen números, flash y sonido?
2. Haz el combo.
3. Sube a la torre y salta: ¿aterrizaje de superhéroe?
4. Siéntate en el banco y pulsa E en la palanca.
5. Escribe `/e dance` y luego `/e flex`: el segundo debe enseñar la lista de emotes.

Apunta lo que falle.

## 7. Jugar con un amigo

**Por qué hace falta un paso antes:** en Studio, cada animación sin publicar recibe un ID temporal que **solo
funciona en el ordenador que la cargó**. Con dos jugadores, cada uno vería al otro sin animaciones. La
solución es publicarlas.

**7.1 Publicar las 27 animaciones** (una vez).

**Forma rápida: un solo comando (recomendada).** El script sube las 27 animaciones a tu cuenta y rellena
`AnimationIds.luau` solo. Necesita una *API key* tuya; solo tú puedes crearla, y se tarda unos 2 minutos:
1. Entra en [create.roblox.com](https://create.roblox.com) → **Open Cloud** → **API Keys** → **Create API Key**.
2. Ponle un nombre, añade la API **Assets** con los permisos **Read** y **Write**, y en *Accepted IP
   Addresses* pon `0.0.0.0/0`. Crea la clave y cópiala (solo se ve una vez).
3. Busca tu **ID de usuario**: es el número de la dirección de tu perfil (`roblox.com/users/123456789/profile`).
4. En PowerShell, en la carpeta del proyecto:
   ```powershell
   $env:ROBLOX_API_KEY = "pega-aqui-la-clave"
   py roblox/publish/publish_animations.py --user-id 123456789
   ```
   (Si el juego es de un grupo, usa `--group-id <id del grupo>` en lugar de `--user-id`.)
   Con `--dry-run` ves qué subiría sin subir nada. Si alguna falla, vuelve a ejecutarlo: las que ya tienen ID
   se saltan.
5. Vuelve a construir el juego (`rojo build -o build/AnimationForge.rbxl`) o deja que `rojo serve` lo sincronice.
   No compartas la clave con nadie; cuando acabes, puedes borrarla en la misma página.

**Forma manual (sin API key), una por una:**
1. Inserta un personaje R15 de prueba, por ejemplo desde el constructor de rigs (*Rig Builder*, pestaña *Avatar*).
2. Abre el **Animation Editor** con ese rig seleccionado.
3. Carga cada animación de `ReplicatedStorage → AnimationPack → KeyframeSequences` (por ejemplo, clic derecho
   sobre la KeyframeSequence → *Save to Roblox*, o cárgala en el editor y usa *Publish to Roblox*).
4. Copia el número de ID que te da Roblox y pégalo en
   [`src/shared/AnimationIds.luau`](src/shared/AnimationIds.luau), en la línea de esa animación
   (`walk = 0,` → `walk = 1234567890,`). Guarda el archivo y Rojo lo sincroniza.
5. **Importante:** las animaciones deben pertenecer al **mismo dueño que el juego**: tu cuenta, o el mismo
   grupo si publicas el juego en un grupo. Si no, no se reproducen.

**7.2 Probar con 2 jugadores en Studio:** en la pestaña *Test*, elige *Clients and Servers* con **2 players**
y pulsa *Start*. Se abren un servidor y dos ventanas de jugador. Prueba el choca esos cinco (`/e highfive`
en los dos a la vez y cerca), los KOs, los sets a 5 y el banco lanzándose el uno al otro.

**7.3 Jugar de verdad con tu amigo:**
1. *File → Publish to Roblox*.
2. El mapa de pruebas solo se construye solo dentro de Studio. Para que también aparezca en el juego publicado,
   selecciona `ReplicatedStorage → AnimationPack`, ve a *Properties → Attributes → +* y añade un atributo
   booleano **`BuildTestArena`** con valor **true**.
3. Pon el juego en público o compártelo con tu amigo, y entrad desde Roblox.

## 8. Si algo falla

Abre *View → Output* y busca los mensajes en rojo.

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Errores rojos en *Output* al pulsar Play | Un fallo que las pruebas automáticas no cubren | Copia el texto completo del error (archivo y línea) y pásamelo; lo corrijo |
| La piscina está vacía (sin agua) o `/e` no hace nada | El lugar no tiene *Terrain* o usa el chat antiguo (pasa con lugares viejos o hechos a mano) | Usa `build/AnimationForge.rbxl` (sección 4) o la plantilla **Baseplate**: el proyecto ya añade Terrain y TextChatService |
| `[AnimationPack] "xxx" has no published ID...` | Animación sin publicar fuera de Studio, o con un ID en 0 | Sección 7.1 |
| El personaje se ve raro o rígido | El lugar usa avatares R6 | Sección 5: elige R15 |
| Rojo no conecta | `rojo serve` no está abierto, o lo bloquea el firewall | Deja la consola abierta, acepta el permiso del firewall y comprueba que el puerto sea 34872 |
| Tu amigo te ve sin animaciones | IDs temporales de Studio | Publica las animaciones (sección 7.1) |
| No suena nada | Los sonidos usan archivos internos de Roblox (`rbxasset://sounds/...`). Si alguno ya no existe, se queda en silencio | Cámbialos por sonidos tuyos en [`src/shared/Feedback.luau`](src/shared/Feedback.luau) |
| La espada se sostiene en un ángulo raro | El agarre se calcula en `CombatServer` y no se ha visto nunca en Studio | Ajusta `SWORD_HANDLE_OFFSET` en [`src/server/CombatServer.server.luau`](src/server/CombatServer.server.luau) |
| Los carteles miran al revés o no se lee el texto | Orientación sin probar en Studio | Ajusta las posiciones en `src/server/TestArena.server.luau` (busca `ControlsSign` y `RecordsBoard`) |

## 9. Comprobar el código y las pruebas automáticas

Con las herramientas de `rokit install` (sección 2):

| Comando | Qué hace |
|---|---|
| `rojo build -o build/AnimationForge.rbxl` | Construye el juego en un archivo que se abre con doble clic |
| `rojo sourcemap default.project.json -o sourcemap.json` y luego `luau-lsp analyze --sourcemap=sourcemap.json --definitions=<globalTypes.d.luau> roblox/src` | Comprueba los tipos de todo el código Luau con la API de Roblox (`globalTypes.d.luau` se descarga del repositorio de luau-lsp) |
| `selene roblox/src` | Linter: errores comunes de Luau/Roblox |
| `python roblox/check_project.py` | Comprueba que las 27 animaciones, sus IDs y sus datos cuadran |
| `python roblox/test/run_tests.py` | **Prueba automática en Studio** (abajo) |

Estado actual: luau-lsp (modo estricto en todos los archivos), selene y `check_project.py` pasan sin
errores ni avisos.

### Prueba automática en Roblox Studio

`python roblox/test/run_tests.py` (o `... solo` / `... multi`):
1. construye un lugar de prueba (`build/AFTest_solo.rbxl` o `build/AFTest_multi.rbxl`);
2. instala el plugin `roblox/test/AFHarness.plugin.luau` en tu carpeta de plugins de Studio. **Solo actúa
   en lugares de prueba** (los que tienen `ReplicatedStorage.__AFTest`), así que no molesta en tus otros juegos;
3. abre Studio, arranca Play (solo, o 2 jugadores con servidor) y **juega**: pega al muñeco con puñetazo,
   combo, patada y espada, bloquea, se agacha, hace los emotes, trepa la torre, salta a la piscina, usa el
   banco, hace el reto del muñeco… Con 2 jugadores también: bloqueo, parry, guard break, sneak attack, KOs,
   provocaciones, ganar un set, choca esos cinco, fiesta de baile, el banco lanzando al amigo y el "dunk";
4. cierra Studio y escribe el informe en `build/test_report_solo.json` / `build/test_report_multi.json`.

Necesita Studio instalado y con la sesión iniciada. **No toques Studio mientras corre** (tarda unos minutos
por modo) y no lances dos pruebas a la vez.

**Resultados (23-11-2026, en este PC):**

| Prueba | Resultado |
|---|---|
| Solo | **64 de 64** correctas: estructura, las 27 animaciones cargan, idle/correr/saltar, agacharse, los 7 emotes, "left hanging", puñetazo (10), combo (30), patada (15, lo empuja), espada (22), patada con espada, bloqueo, KO del muñeco con su muerte y reaparición, reto de 10 s, aterrizaje de superhéroe, piscina (salpicadura, récord, nadar), zambullida fuerte, carrera de escalada con récord, salto desde la torre, banco lanzador, tablón y muerte del jugador |
| 2 jugadores | **27 de 27** correctas: puñetazo, bloqueo, parry, guard break, sneak attack, 5 KOs y set ganado con cheer, provocación, choca esos cinco, fiesta de baile, banco lanzando al amigo, dunk en la piscina y tablón |
| Errores de scripts | **0** errores y 0 avisos, en el servidor y en los clientes, en las dos pruebas |

**Bugs reales que encontraron las pruebas (ya arreglados):**
- El servidor comprobaba la altura de caída antes de recibir la posición real del jugador (retraso de red),
  así que se perdían los aterrizajes de superhéroe y las salpicaduras. Ahora espera 0,3 s y lo compara con
  su historial de alturas.
- Si el banco te lanzaba fuerte, a veces llegabas al fondo de la piscina antes de que Roblox detectara que
  nadabas: salía un aterrizaje de superhéroe bajo el agua y **no contaba la salpicadura** (ni el récord).
  Ahora, aterrizar dentro del agua cuenta como salpicadura. Hay un test que lo reproduce (3 zambullidas
  fuertes) y que fallaba antes del arreglo.

**Límites conocidos:**
- Con 2 jugadores y las animaciones **sin publicar**, cada uno ve al otro **sin animaciones** (en Studio, los
  IDs temporales solo valen en el ordenador que los crea). Se arregla publicándolas (sección 7.1).
- Studio no deja que un plugin simule el teclado y el ratón de verdad, así que la prueba llama a las mismas
  acciones por los ganchos `PackAction` de `CombatInput` y `Animate` (los mismos que usan las teclas, el mando
  y los botones táctiles).
- Enviar un mensaje de chat se queda bloqueado dentro de las pruebas de Studio, así que el `/e` por chat solo
  se comprueba por estructura (que el comando existe y sustituye al de Roblox). Los emotes en sí sí se prueban.
- Una animación de duración 0 llamada `Animation1` que aparece en el personaje es del propio avatar de Roblox (la cara). No afecta.

## 10. Siguientes pasos

Según la simulación de los dos amigos (`playtest/REPORT.md`), lo que más falta para que vuelvan a jugar es:
- **progresión**: cosas que desbloquear, tienda, segundo mapa
- **equilibrar la espada**: ahora "gana quien hace clic primero"

Cuando lo tengas funcionando, dime qué falló y cuál quieres hacer.

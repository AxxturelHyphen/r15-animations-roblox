# Guía: jugar el proyecto en tu PC

Esta guía va desde cero hasta jugar solo en Roblox Studio, jugar con un amigo y publicar el juego.
Los detalles técnicos están en [`README.md`](README.md).

## 1. Qué vas a tener al final

- **Un prototipo jugable**: un mapa de pruebas con combate (puñetazo, combo, patada, espada, bloqueo y parry),
  KOs y sets a 5 contra tu amigo, tablón de récords, un banco que te lanza a la piscina, una carrera de escalada,
  un muñeco de entrenamiento, emotes y el choca esos cinco.
- **27 animaciones R15 propias**, que sustituyen a las de Roblox (andar, correr, saltar, nadar, trepar, sentarse…).
- **Aviso:** el código **nunca se ha ejecutado dentro de Roblox Studio**. Se revisó leyéndolo, pero no se
  pudo probar en el entorno donde se escribió. Es normal que la primera vez salga algún error en la ventana
  *Output*. La sección 8 explica qué hacer.

## 2. Qué necesitas instalar

| Herramienta | Para qué | Cómo conseguirla |
|---|---|---|
| **Roblox Studio** | Abrir y probar el juego | Desde create.roblox.com, con tu cuenta de Roblox |
| **Git** | Descargar el proyecto | git-scm.com (en Windows, "Git for Windows") |
| **Rojo 7** | Sincronizar los archivos del proyecto con Studio | Ver abajo |

**Rojo, la forma más fácil:** instala **Visual Studio Code** y, dentro de él, la extensión **Rojo**
(de evaera). La extensión instala el programa `rojo` y el plugin de Rojo para Studio, y te deja iniciar el
servidor con un clic.

**Rojo, alternativa por consola:** instala [Aftman](https://github.com/LPGhatguy/aftman) y ejecuta
`aftman add rojo-rbx/rojo@7.4.4` en la carpeta del proyecto. El plugin de Studio se instala aparte, desde la
página de Rojo (rojo.space) o con `rojo plugin install`.

En macOS los pasos son los mismos. Los comandos se escriben en *Terminal* en lugar de *PowerShell*.

## 3. Descargar el proyecto

En PowerShell (Windows) o Terminal (Mac):

```bash
git clone https://github.com/AxxturelHyphen/file_sorter.git
cd file_sorter
git checkout guija/festive-turing-kfdsdv   # cuando el PR esté fusionado, basta con la rama master
```

Las carpetas que importan:
- `default.project.json`: le dice a Rojo dónde va cada cosa dentro de Studio.
- `roblox/src/`: el código del juego (Luau).
- `output/rbxmx/`: las 27 animaciones, como KeyframeSequences.

## 4. Conectar Studio con Rojo

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

| Acción | Tecla | Qué deberías ver |
|---|---|---|
| Moverse / saltar | WASD / Espacio | Animaciones propias de andar o correr. Al caer desde 18+ studs (desde la torre): **aterrizaje de superhéroe**, con polvo y un golpe sordo |
| Agacharse | C o Ctrl izquierdo | Pose de sigilo, andar lento. Golpear a alguien **por la espalda** agachado hace **SNEAK ATTACK x2** |
| Puñetazo / combo | Clic / clic otra vez rápido | Flash, número de daño, parón breve (hit-stop). El 3.er golpe del combo es **GUARD BREAK** y atraviesa el bloqueo |
| Patada | Q | Manda volando al objetivo, por ejemplo desde la torre o a la piscina ("dunked") |
| Bloquear / parry | Mantener F / pulsar F justo antes del golpe | "BLOCKED" con clang. Si lo pulsas justo a tiempo: **PARRY!**, y el atacante se tambalea |
| Espada | 1, luego clic | Tajo diagonal con lunge, 22 de daño |
| Emotes | Chat: `/e wave`, `dance`, `cheer`, `point`, `laugh`, `clap`, `salute` | El emote. Si escribes uno que no existe, el chat te da la lista |
| Banco lanzador | Siéntate en el banco; tú u otro jugador pulsáis **E** en la palanca ("Launch!") | Vuelas en arco a la piscina, con una altura distinta cada vez, y una salpicadura que puede batir el récord |
| Carrera de escalada | Pisa la plataforma verde, trepa y toca la campana | Tu tiempo, y "NEW RECORD!" si lo bates |
| Reto del muñeco | **E** en la plataforma naranja ("10 s damage challenge") | Cuenta atrás de 10 s; al final, tu daño total y el récord |

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

**7.1 Publicar las 27 animaciones** (una vez):
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
| Errores rojos en *Output* al pulsar Play | Un fallo del código, que nunca se ha ejecutado en Studio | Copia el texto completo del error (archivo y línea) y pásamelo; lo corrijo |
| `[AnimationPack] "xxx" has no published ID...` | Animación sin publicar fuera de Studio, o con un ID en 0 | Sección 7.1 |
| El personaje se ve raro o rígido | El lugar usa avatares R6 | Sección 5: elige R15 |
| Rojo no conecta | `rojo serve` no está abierto, o lo bloquea el firewall | Deja la consola abierta, acepta el permiso del firewall y comprueba que el puerto sea 34872 |
| Tu amigo te ve sin animaciones | IDs temporales de Studio | Publica las animaciones (sección 7.1) |
| No suena nada | Los sonidos usan archivos internos de Roblox (`rbxasset://sounds/...`). Si alguno ya no existe, se queda en silencio | Cámbialos por sonidos tuyos en [`src/shared/Feedback.luau`](src/shared/Feedback.luau) |
| La espada se sostiene en un ángulo raro | El agarre se calcula en `CombatServer` y no se ha visto nunca en Studio | Ajusta `SWORD_HANDLE_OFFSET` en [`src/server/CombatServer.server.luau`](src/server/CombatServer.server.luau) |
| Los carteles miran al revés o no se lee el texto | Orientación sin probar en Studio | Ajusta las posiciones en `src/server/TestArena.server.luau` (busca `ControlsSign` y `RecordsBoard`) |

## 9. Opcional: comprobar el código

En mi entorno no se pudieron instalar estas herramientas. En tu PC sí puedes usarlas:
- **luau-analyze** (de github.com/luau-lang/luau) detecta errores de tipos: `luau-analyze roblox/src`.
- **selene** (por ejemplo con `aftman add Kampfkarren/selene`) detecta errores comunes: `selene roblox/src`.
- **Comprobación del proyecto** (necesita Python): `python roblox/check_project.py`.

## 10. Siguientes pasos

Según la simulación de los dos amigos (`playtest/REPORT.md`), lo que más falta para que vuelvan a jugar es:
- **progresión**: cosas que desbloquear, tienda, segundo mapa
- **equilibrar la espada**: ahora "gana quien hace clic primero"

Cuando lo tengas funcionando, dime qué falló y cuál quieres hacer.

extends CharacterBody2D

const SPEED = 30.0
var direction = Vector2.ZERO
var estado = "parado"

var estados_possiveis = ["andando", "comendo", "descansar"]

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var timer: Timer = $Timer



func _ready():
	randomize()
	decidir_proxima_acao()

func _physics_process(delta: float) -> void:
	if estado == "andando":
		velocity = direction * SPEED
		move_and_slide()

		if direction != Vector2.ZERO:
			animated_sprite_2d.play("walk")
			animated_sprite_2d.flip_h = direction.x < 0
		else:
			animated_sprite_2d.play("Idle")
	else:
		velocity = Vector2.ZERO

func decidir_proxima_acao():
	estado = estados_possiveis[randi() % estados_possiveis.size()]

	if estado == "andando":
		andar()
	elif estado == "comendo":
		comendo()
	elif estado == "descansar":
		descansar()

func andar():
	var direcoes = [Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN]
	direction = direcoes[randi() % direcoes.size()]
	timer.start(randf_range(1.5, 4.0))  
	await timer.timeout
	direction = Vector2.ZERO
	estado = "parado"
	decidir_proxima_acao()

func comendo():
	animated_sprite_2d.play("comendo")  
	timer.start(randf_range(1.0, 3.0))  
	await timer.timeout
	estado = "parado"
	decidir_proxima_acao()

func descansar():
	animated_sprite_2d.play("Idle")
	timer.start(randf_range(2.0, 6.0))  
	await timer.timeout
	estado = "parado"
	decidir_proxima_acao()

extends CharacterBody2D

const SPEED = 30.0
var direction = Vector2.ZERO
var mudanca_direcao = 0.0
const intervalo_mudanca_direcao = 2.0

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D

func _ready():
	randomize()
	_pick_new_direction()

func _physics_process(delta: float) -> void:
	mudanca_direcao -= delta
	if mudanca_direcao <= 0.0:
		_pick_new_direction()

	velocity = direction * SPEED
	move_and_slide()

	if direction == Vector2.ZERO:
		animated_sprite_2d.play("Idle")
	else:
		animated_sprite_2d.play("walk")
		animated_sprite_2d.flip_h = direction.x < 0  
func _pick_new_direction():
	var directions = [
		Vector2.LEFT,
		Vector2.RIGHT,
		Vector2.UP,
		Vector2.DOWN,
		Vector2.ZERO
	]
	direction = directions[randi() % directions.size()]
	mudanca_direcao = intervalo_mudanca_direcao

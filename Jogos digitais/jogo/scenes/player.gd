extends CharacterBody2D

var SPEED = 300
var GRAVITY = 980
var JUMP_VELOCITY = -400

func _ready():
	pass
	
func _process(delta: float) -> void:
#	gravidade
	velocity.y += GRAVITY * delta
#	move de acordo com o valor armazenado em velocity
	move_and_slide()
	

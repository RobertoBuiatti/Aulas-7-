extends CharacterBody2D

class_name fantasmaChao

signal enimy

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var anim: AnimationPlayer = $AnimEnimy

const SPEED := 50.0
var direction := -1
const JUMP_VELOCITY = -400.0
var GRAVITY = 980

func _physics_process(delta: float) -> void:
	velocity.y += GRAVITY * delta
		
	velocity.x = direction * SPEED
	if is_on_wall():
		global_position.x += direction * -2  # Dá um "empurrãozinho" para trás
		direction *= -1
		
	if direction != 0:	
		anim.play("andar")
		
	if direction < 0:
		sprite_2d.flip_h = false
	elif direction > 0:
		sprite_2d.flip_h = true

	move_and_slide()


func _on_area_2d_body_entered(body: Node2D) -> void:
	enimy.emit()

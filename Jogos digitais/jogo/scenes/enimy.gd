extends CharacterBody2D
@onready var sprite_2d: Sprite2D = $Sprite2D

@onready var anim: AnimationPlayer = $AnimEnimy
const SPEED := 50.0
var direction := -1
const JUMP_VELOCITY = -400.0


func _physics_process(delta: float) -> void:
	# Add the gravity.
	if not is_on_floor():
		velocity += get_gravity() * delta
		
		
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

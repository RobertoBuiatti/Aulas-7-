extends CharacterBody2D


const SPEED = 150.0
var dir = "down"
@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D


func _physics_process(delta: float) -> void:

	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction := Input.get_vector("ui_left", "ui_right","ui_up","ui_down")
	velocity = direction * SPEED
	
	if direction.y > 0:
		dir = "down"
	elif direction.y < 0:
		dir = "up"
	elif direction.x > 0:
		dir = "right"
	elif direction.x < 0:
		dir =  "left"

	if direction.x == 0 and direction.y == 0:	
		animated_sprite_2d.play("idle-" + dir)
	else:
		animated_sprite_2d.play("walk-" + dir)

	move_and_collide(velocity * delta)

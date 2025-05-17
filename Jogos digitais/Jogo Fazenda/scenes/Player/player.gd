extends CharacterBody2D


const SPEED = 300.0
var dir: Vector2 = Vector2.ZERO


func _physics_process(delta: float) -> void:

	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction := Input.get_vector("ui_left", "ui_right","ui_up","ui_down")
	velocity = direction * SPEED
		

	move_and_slide()

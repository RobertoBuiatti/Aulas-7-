extends CharacterBody2D
@onready var Sprite_2d: Sprite2D = $Sprite2D
@onready var anim: AnimationPlayer = $Anim
@onready var respawn_point: Vector2 = global_position

var SPEED = 300
var GRAVITY = 980
var JUMP_VELOCITY = -400
var jumps = 0
var max_jumps = 1
var double_jump = false


func _ready():
	pass
	
func _process(delta: float) -> void:
#	gravidade
	velocity.y += GRAVITY * delta
#	move de acordo com o valor armazenado em velocity

#movimento horizontal
	var direction = Input.get_axis("walk_left", "walk_right")
	velocity.x = direction * SPEED
	var jump = Input.is_action_just_pressed("jump")
# pulo
	#if Input.is_action_just_pressed("jump") and (is_on_floor() or double_jump == false):
		#velocity.y = JUMP_VELOCITY
		#if is_on_floor():
			#double_jump = false
		#else:
			#double_jump = true
	
#	olhe para o lado que esta andando
	if direction > 0:
		Sprite_2d.flip_h = false
	elif direction < 0:
		Sprite_2d.flip_h = true
		
	if direction != 0:	
		anim.play("walk")
	else:
		anim.play("idle")
# premitir pulo duplo
	if jump and jumps < max_jumps:
		velocity.y = JUMP_VELOCITY
		jumps +=1
	if is_on_floor():
		jumps = 0
	else:
		if velocity.y < 0:
			anim.play("jump")
		else:
			anim.play("fall")
		
	move_and_slide()
	
	
	if global_position.y > 1000:
		respawn()
		
		
#		função de respawn
func respawn()->void:
	global_position = respawn_point
	velocity = Vector2.ZERO

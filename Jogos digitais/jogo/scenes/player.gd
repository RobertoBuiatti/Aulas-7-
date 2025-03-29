extends CharacterBody2D
@onready var Sprite_2d: Sprite2D = $Sprite2D
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
# premitir pulo duplo
	if Input.is_action_just_pressed("jump") and jumps < max_jumps:
		velocity.y = JUMP_VELOCITY
		jumps +=1
	if is_on_floor():
		jumps = 0
	move_and_slide()
	

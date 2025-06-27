extends CharacterBody2D

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var marker_2d: Marker2D = $Marker2D

var speed = 100
var player_state
@export var inv: Inv

var bow_equiped = false
var bow_cooldown = true
var arrow = preload("res://scene/arrow.tscn")
var mouse_loc_from_player = null
var is_attacking = false

func _ready():
	animated_sprite_2d.animation_finished.connect(_on_animation_finished)

func _physics_process(delta):
	mouse_loc_from_player = get_global_mouse_position() - self.position
	var direction = Input.get_vector("left", "right", "up", "down")

	# Player pode andar mesmo durante ataque
	velocity = direction * speed
	move_and_slide()

	# Define estado (usado só se quiser animar movimento fora do ataque)
	if direction.length() == 0:
		player_state = "idle"
	else:
		player_state = "walking"

	# Alterna o arco
	if Input.is_action_just_pressed("e"):
		bow_equiped = !bow_equiped

	marker_2d.look_at(get_global_mouse_position())

	# Inicia ataque (mas não bloqueia movimento)
	if Input.is_action_just_pressed("left_mouse") and bow_equiped and bow_cooldown and !is_attacking:
		is_attacking = true
		bow_cooldown = false
		play_attack_animation()
		shoot_arrow_later()

	play_anim(direction)

# Função que solta a flecha 0.2s após início do ataque
func shoot_arrow_later():
	await get_tree().create_timer(0.2).timeout
	var arrow_instance = arrow.instantiate()
	arrow_instance.rotation = marker_2d.rotation
	arrow_instance.global_position = marker_2d.global_position
	add_child(arrow_instance)

func play_attack_animation():
	if mouse_loc_from_player.x >= -25 and mouse_loc_from_player.x <= 25 and mouse_loc_from_player.y < 0:
		animated_sprite_2d.play("n-attack")
	elif mouse_loc_from_player.y >= -25 and mouse_loc_from_player.y <= 25 and mouse_loc_from_player.x > 0:
		animated_sprite_2d.play("e-attack")
	elif mouse_loc_from_player.x >= -25 and mouse_loc_from_player.x <= 25 and mouse_loc_from_player.y > 0:
		animated_sprite_2d.play("s-attack")
	elif mouse_loc_from_player.y >= -25 and mouse_loc_from_player.y <= 25 and mouse_loc_from_player.x < 0:
		animated_sprite_2d.play("w-attack")
	elif mouse_loc_from_player.x >= 25 and mouse_loc_from_player.y <= -25:
		animated_sprite_2d.play("ne-attack")
	elif mouse_loc_from_player.x >= 0.5 and mouse_loc_from_player.y >= 25:
		animated_sprite_2d.play("se-attack")
	elif mouse_loc_from_player.x <= -0.5 and mouse_loc_from_player.y >= 25:
		animated_sprite_2d.play("sw-attack")
	elif mouse_loc_from_player.x <= -25 and mouse_loc_from_player.y <= -25:
		animated_sprite_2d.play("nw-attack")

func _on_animation_finished():
	# Libera novo ataque apenas quando animação terminar
	if is_attacking:
		await get_tree().create_timer(0.1).timeout  # leve delay antes de permitir novo
		is_attacking = false
		bow_cooldown = true

func play_anim(dir):
	# Se estiver atacando, mantém a animação de ataque atual até ela acabar
	if is_attacking:
		return

	if !bow_equiped:
		if player_state == "idle":
			animated_sprite_2d.play("idle")
		elif player_state == "walking":
			play_walk_animation(dir)
	else:
		# Arco equipado mas não atacando
		if player_state == "idle":
			animated_sprite_2d.play("idle")
		elif player_state == "walking":
			play_walk_animation(dir)

func play_walk_animation(dir):
	if dir.y == -1:
		animated_sprite_2d.play("n-walk")
	elif dir.x == 1:
		animated_sprite_2d.play("e-walk")
	elif dir.y == 1:
		animated_sprite_2d.play("s-walk")
	elif dir.x == -1:
		animated_sprite_2d.play("w-walk")
	elif dir.x > 0.5 and dir.y < -0.5:
		animated_sprite_2d.play("ne-walk")
	elif dir.x > 0.5 and dir.y > 0.5:
		animated_sprite_2d.play("se-walk")
	elif dir.x < -0.5 and dir.y > 0.5:
		animated_sprite_2d.play("sw-walk")
	elif dir.x < -0.5 and dir.y < -0.5:
		animated_sprite_2d.play("nw-walk")

func player():
	pass

func collect(item):
	inv.insert(item)

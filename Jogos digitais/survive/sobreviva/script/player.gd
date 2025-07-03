extends CharacterBody2D

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var marker_2d: Marker2D = $Marker2D

var victory_label: Label
var speed = 100
var player_state
var health = 100
var enemy_inattack_range = false
var enemy_attack_cooldown = true
var player_alive = true
@export var inv: Inv

var bow_equiped = false
var bow_cooldown = true
var arrow = preload("res://scene/arrow.tscn")
var mouse_loc_from_player = null
var is_attacking = false

func _ready():
	animated_sprite_2d.animation_finished.connect(_on_animation_finished)
	victory_label = get_node("/root/world/CanvasLayer/VictoryLabel")
	victory_label.visible = false

func _physics_process(delta):
	mouse_loc_from_player = get_global_mouse_position() - self.position
	var direction = Input.get_vector("left", "right", "up", "down")

	velocity = direction * speed
	move_and_slide()

	
	if direction.length() == 0:
		player_state = "idle"
	else:
		player_state = "walking"

	
	if Input.is_action_just_pressed("e"):
		bow_equiped = !bow_equiped

	marker_2d.look_at(get_global_mouse_position())

	
	if Input.is_action_just_pressed("left_mouse") and bow_equiped and bow_cooldown and !is_attacking:
		is_attacking = true
		bow_cooldown = false
		play_attack_animation()
		shoot_arrow_later()
	
	enemy_attack()
	update_health()
	play_anim(direction)


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
	
	if is_attacking:
		await get_tree().create_timer(0.1).timeout  
		is_attacking = false
		bow_cooldown = true

func play_anim(dir):
	
	if is_attacking:
		return

	if !bow_equiped:
		if player_state == "idle":
			animated_sprite_2d.play("idle")
		elif player_state == "walking":
			play_walk_animation(dir)
	else:
		
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

var apple_count: int = 0
var slime_count: int = 0

func collect(item):
	inv.insert(item)
	if item.name == "apple":
		apple_count += 1
	elif item.name == "slime":
		slime_count += 1
	check_goal()

func check_goal():
	if apple_count >= 5 and slime_count >= 5:  
		victory_label.visible = true
		await get_tree().create_timer(3).timeout  
		get_tree().reload_current_scene()  


func update_health():
	var healthbar = $healthbar
	healthbar.value = health
	
	if health >= 100:
		healthbar.visible = false
	else:
		healthbar.visible = true

func _on_regin_timer_timeout() -> void:
	if health < 100:
		health = health + 20
		if health > 100:
			health = 100
	if health <= 0:
		health = 0


func _on_player_hitbox_body_entered(body: Node2D) -> void:
	if body.has_method("enemy"):
		enemy_inattack_range = true


func _on_player_hitbox_body_exited(body: Node2D) -> void:
	if body.has_method("enemy"):
		enemy_inattack_range = false


func enemy_attack():
	if enemy_inattack_range:
		print("player")
	pass

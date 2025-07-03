extends CharacterBody2D

@onready var detection_area: CollisionShape2D = $detection_area/CollisionShape2D
@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var hitbox: CollisionShape2D = $hitbox/CollisionShape2D
@onready var slime_collect_area: CollisionShape2D = $slime_collect_area/CollisionShape2D

var speed = 50.0
var health = 100
var knockback_timer = 0.0
var knockback_duration = 0.2

var dead = false
var player_in_area = false
var player

@onready var slime: StaticBody2D = $slime_collectable
@export var itemRes: InvItem

func _ready():
	dead = false
	
	if has_node("push_area"):
		$push_area.body_entered.connect(_on_push_area_body_entered)

func _physics_process(delta):
	if knockback_timer > 0:
		knockback_timer -= delta
		move_and_slide()
		return

	if !dead:
		detection_area.disabled = false
		if knockback_timer <= 0:
			if player_in_area:
				var direction = (player.position - position).normalized()
				velocity = direction * speed
				animated_sprite_2d.play("move")
			else:
				velocity = Vector2.ZERO
				animated_sprite_2d.play("idle")
		move_and_slide()
	else:
		detection_area.disabled = true
		velocity = Vector2.ZERO
		move_and_slide()

func _on_detection_area_body_entered(body: Node2D) -> void:
	if body.has_method("player"):
		player_in_area = true
		player = body


func _on_detection_area_body_exited(body: Node2D) -> void:
	if body.has_method("player"):
		player_in_area = false
		player = body


func _on_hitbox_area_entered(area: Area2D) -> void:
	var damage
	if area.has_method("arrow_deal_damage"):
		damage = 50
		take_damage(damage)

func take_damage(damage):
	health = health - damage
	if health <=0 and !dead:
		death()

func death():
	dead = true
	animated_sprite_2d.play("death")
	await get_tree().create_timer(1).timeout
	drop_slime()
	
	animated_sprite_2d.visible = false
	hitbox.disabled = true
	detection_area.disabled = true

func drop_slime():
	slime.visible = true
	slime_collect_area.disabled = false
	slime_collect()
	
func slime_collect():
	await get_tree().create_timer(1.5).timeout
	slime.visible = false
	player.collect(itemRes)
	queue_free()


func _on_slime_collect_area_body_entered(body: Node2D) -> void:
	if body.has_method("player"):
		player = body

func enemy():
	pass

func apply_knockback(new_velocity: Vector2):
	velocity = new_velocity
	knockback_timer = knockback_duration


var push_cooldown := {}

func _on_push_area_body_entered(body: Node2D) -> void:
	if dead:
		return
	var now = Time.get_ticks_msec()
	var id = str(body.get_instance_id())
	if push_cooldown.has(id) and now - push_cooldown[id] < 300:
		return 
	push_cooldown[id] = now

	if body == null or not body.has_method("get_position"):
		return
	var direction = (body.position - position).normalized()
	var push_strength = 400

	
	if body.has_method("enemy"):
		apply_knockback(-direction * push_strength)
		if body.has_method("apply_knockback"):
			body.apply_knockback(direction * push_strength)
		elif body.has_variable("velocity"):
			body.velocity += direction * push_strength
	
	elif body.has_method("player"):
		
		if body.has_method("apply_knockback"):
			body.apply_knockback(direction * push_strength)
		elif body.has_variable("velocity"):
			body.velocity += direction * push_strength
		
		if body.has_method("take_damage"):
			body.take_damage(10)
		elif body.has_variable("health"):
			body.health -= 10

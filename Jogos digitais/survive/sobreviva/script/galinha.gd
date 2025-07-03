extends CharacterBody2D

@onready var detection_area: CollisionShape2D = $detection_area/CollisionShape2D
@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var hitbox: CollisionShape2D = $hitbox/CollisionShape2D
var game_over_label: Label


var speed = 50.0
var knockback_timer = 0.0
var knockback_duration = 0.2
var health = 200

var dead = false
var player_in_area = false
var player

@export var itemRes: InvItem

func _ready():
	dead = false
	game_over_label = get_node("/root/world/CanvasLayer/GameOverLabel")
	game_over_label.visible = false

func _physics_process(delta):
	if knockback_timer > 0:
		knockback_timer -= delta
		move_and_slide()
		return
		
	if !dead:
		detection_area.disabled = false
		if player_in_area:
			var direction = (player.position - position).normalized()
			velocity = direction * speed
			move_and_slide()

			if abs(direction.x) > abs(direction.y):
				if direction.x > 0:
					animated_sprite_2d.play("e-walk")
				else:
					animated_sprite_2d.play("w-walk")
			else:
				if direction.y > 0:
					animated_sprite_2d.play("s-walk")
				else:
					animated_sprite_2d.play("n-walk")
		else:
			velocity = Vector2.ZERO
			move_and_slide()
			animated_sprite_2d.play("idle")
	else:
		detection_area.set_deferred("disabled", true)
		velocity = Vector2.ZERO
		move_and_slide()
		animated_sprite_2d.play("death")
		game_over_label.visible = true

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
		damage = 60
		take_damage(damage)

func take_damage(damage):
	health = health - damage
	if health <= 150:
		death()

func death():
	dead = true
	animated_sprite_2d.play("death")
	hitbox.set_deferred("disabled", true)
	detection_area.set_deferred("disabled", true)
	game_over_label.visible = true
	
	await get_tree().create_timer(2.0).timeout 
	get_tree().quit()

func apply_knockback(new_velocity: Vector2):
	velocity = new_velocity

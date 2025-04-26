extends CharacterBody2D

class_name fantasmaVoando

signal take_damage

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var anim: AnimationPlayer = $AnimEnimy

const SPEED := 50.0
var direction := -1
var time := 0.0  # Tempo acumulado para o movimento de voo

func _physics_process(delta: float) -> void:
	# Movimento horizontal
	velocity.x = direction * SPEED

	# Movimento vertical de voo com função seno
	time += delta
	velocity.y = sin(time * 2.0) * 20  # frequência * amplitude

	# Inverte direção ao bater na parede
	if is_on_wall():
		global_position.x += direction * -2
		direction *= -1

	# Toca animação de andar
	if direction != 0:
		anim.play("andar")

	# Espelha o sprite
	sprite_2d.flip_h = direction > 0

	# Move o inimigo com a velocidade calculada
	move_and_slide()


func _on_area_2d_body_entered(body: Node2D) -> void:
	print("FASTASMA")
	take_damage.emit()

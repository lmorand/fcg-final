# 6. Surface Normals and Multiple Objects

## 6.3-6.4:

- No existe entidad `hit_record`, solo se devuelven los datos en `hit`.

## 6.5:

- `HittableList` podría ser algo como `World`.

# 7. Antialiasing

## 7.2:

- ¿Se podría evitar el último for cuando el rayo no choca con nada? Probablemente ocasionaría que se pierda el antialiasing del fondo.

- ¿Usar otra distribución que no sea uniforme?

# 8. Diffuse Materials

## 8.2:

- Se volvió terriblemente lento.

- Al parecer sale más obscuro que en el libro.

	![`samples_per_pixel = 10` y `max_depth = 50`](0_spp10_md50.png)

	![`samples_per_pixel = 100` y `max_depth = 5`](1_spp100_md5.png)

	- Según el libro es por la corrección gamma, pero no me convence.
	- En efecto, la corrección gamma parece haberlo acomodado.

## 8.5-8.6:

- Me voy a quedar con la reflexión lambertiana.

- 
	>Scenes will become more complicated over the course of the book. You are encouraged to switch
	>between the different diffuse renderers presented here. Most scenes of interest will contain a
	>disproportionate amount of diffuse materials. You can gain valuable insight by understanding
	>the effect of different diffuse methods on the lighting of the scene.

	¿Modularizar renderers?
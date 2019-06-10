--@Buscar personas por nombre y determina si son amigos o no. (Estado 2 = Aceptado)

SELECT u.id, u.nombres, u.apellidos, (select count(*)<0 from invitacion i where i.idusuario_invita = 1 and i.idusuario_invitado = u.id and i.estado = 2) as friends
    from usuario u
    where u.nombres LIKE 'Maria' or u.apellidos LIKE 'Maria' order by u.nombres desc
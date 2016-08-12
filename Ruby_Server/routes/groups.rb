post '/api/novoGrupo' do
	body = JSON.parse request.body.read
	response = Hash.new
	id_admin = body['idAdmin']
	group_name = body['nome']
	icon_url = body['icone']

	group = Group.create(
				admin: id_admin,
				name: group_name,
				icon_url: icon_url
			)

	user = User.first(id: id_admin)

	group.users << user
	group.save

	if group.saved?
		response[:sucesso] = 'S'
	    response[:idGrupo] = group.id
	else
	    response[:sucesso] = 'N'
	    response[:idGrupo] = nil
	end

	status 201
  	format_response(response, request.accept)
end

post '/api/adicionarUsuarioGrupo' do
	body = JSON.parse request.body.read
	response = Hash.new
	id_admin = body['idAdmin']
	id_user = body['idUsuario']
	id_group = body['idGrupo']

	group = Group.first(id: id_group)

	if group.admin == id_admin
		user = User.first(id: id_user)
		group.users << user
		group.save
		added = true
	else
		added = false
	end
	if added
		response[:sucesso] = "S"
	else
		response[:sucesso] = "N"
	end

	status 201
  	format_response(response, request.accept)
end

post '/api/removerUsuarioGrupo' do
	body = JSON.parse request.body.read
	response = Hash.new
	id_admin = body['idAdmin']
	id_user = body['idUsuario']
	id_group = body['idGrupo']

	group = Group.first(id: id_group)

	if group.admin == id_admin
		user = User.first(id: id_user)
		link = GroupUser.get(group.id, user.id)
		link.destroy
		removed = true
	else
		removed = false
	end
	if removed
		response[:sucesso] = "S"
	else
		response[:sucesso] = "N"
	end

	status 201
  	format_response(response, request.accept)
end

post '/api/excluirGrupo' do
	body = JSON.parse request.body.read
	response = Hash.new
	id_user = body['idUsuario']
	id_group = body['idGrupo']

	group = Group.first(id: id_group)
	group_users = group.users

	if group.admin == id_user
		group_users.each do |g|			
			user = User.first(id: g.id)
			link = GroupUser.get(group.id, g.id)
			link.destroy
		end
		remove = group.destroy
		removed = true
	else
		removed = false
	end
	if removed
		remove = group.destroy
		if remove
			response[:sucesso] = "S"
		else
			response[:sucesso] = "N"
		end
	else
		response[:sucesso] = "N"
	end

	status 201
  	format_response(response, request.accept)
end

get '/api/gruposUsuario/:id' do
	response = Array.new
	user = User.first(id: params[:id])
	group_users ||= GroupUser.all(user_id: user.id) || halt(404)
	group_users.each do |g|
		group = g.group
		p group
		group_users = group.users
		temp_hash = Hash.new
		temp_hash[:group] = group
		temp_hash[:users] = group_users
		response << temp_hash 
	end
	format_response(response, request.accept)
end

post '/api/administracaoGrupo' do
	body = JSON.parse request.body.read
	response = Hash.new
	id_admin = body['idAdmin']
	id_user = body['idUsuario']
	id_group = body['idGrupo']
	has_key = false
	group = Group.first(id: id_group)

	if group.admin == id_admin
		group_users = group.users
		group_users.each do |g|
			if g.id == id_user
				has_key = true
				next
			end
		end
		if has_key
			group.update(admin: id_user) 
			added = true
		else
			added = false
		end
	else
		added = false
	end
	if added
		response[:sucesso] = "S"
	else
		response[:sucesso] = "N"
	end

	status 201
  	format_response(response, request.accept)
end

get '/api/group/:id' do
	response = Hash.new
	group ||= Group.get(params[:id]) || halt(404)
	response[:group] = group
	response[:users] = group.users

	format_response(response, request.accept)
end
# encoding: UTF-8

post '/api/usuario' do # Check if there is the device_token in the database
  body = JSON.parse request.body.read

  device = body['device_token']
  os = body['sistema']
  
  answer = Array.new
  answer = check_on_db(device, os) # This method verifies if the user is registered, it returns true or false and the id

  status 201
  response = Hash.new

  if answer.first
    response[:sucesso] = 'S'
    response[:idUsuario] = answer.last
  else
    response[:sucesso] = 'N'
    response[:idUsuario] = answer.last
  end

  format_response(response, request.accept)
end

get '/api/usuarios' do
  format_response(User.all, request.accept)
end

get '/api/usuario/:id' do
  user ||= User.get(params[:id]) || halt(404)
  format_response(user, request.accept)
end

post '/api/criarUsuario' do
  body = JSON.parse request.body.read
  user = User.create(
    device_token:    body['device_token'],
    os_type: body['os_type'],
    encryption_type: body['encryption_type'],
    name:     body['name'],
    email: body['email']
  )
  status 201
  format_response(user, request.accept)
end

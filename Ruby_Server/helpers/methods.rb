def check_on_db(device, os)
	user = User.first(:device_token => device, :os_type => os)
	p user
	if user.nil?
		return [false,nil]
	else
		return [true,user.id]
	end
end
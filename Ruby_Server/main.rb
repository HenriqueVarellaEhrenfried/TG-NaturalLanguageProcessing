# encoding: UTF-8
require 'json'
require 'sinatra'
require 'data_mapper'
require 'dm-core'
require 'dm-migrations'
require 'sinatra/cross_origin'

configure :development do
	enable :cross_origin
	DataMapper::Logger.new($stdout, :debug)
	DataMapper.setup(:default, {
					:adapter  => 'postgres',
					:database => 'restSinatraDev',
					:username => 'postgres',
					:password => '123456',
					:host     => 'localhost'
	})
end

configure :production do
	enable :cross_origin
	DataMapper::Logger.new($stdout, :debug)
	DataMapper.setup(:default, {
					:adapter  => 'postgres',
					:database => 'restSinatraProd',
					:username => 'postgres',
					:password => '123456',
					:host     => 'localhost'
	})
end

configure { set :server, :puma }

require './helpers/init'
require './routes/init'

DataMapper.finalize

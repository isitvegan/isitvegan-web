Vagrant.configure('2') do |config|
  config.vm.box = 'generic/fedora28'

  config.vm.network :forwarded_port, guest: 9200, host: 9200, host_ip: '127.0.0.1'

  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.provider :virtualbox do |vb|
    vb.memory = "3072"
  end

  config.vm.provision :shell, path: 'scripts/setup_vm.sh'
end

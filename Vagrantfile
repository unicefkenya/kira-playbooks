# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "trusty64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"


  config.vm.define "kobo_dev" do |machine|
    machine.vm.network :private_network, ip: "", type: "dhcp"
    machine.vm.network :private_network, ip: "10.0.1.100",
                       :netmask => "255.255.255.0",
                       :adapter => 2
    machine.vm.hostname = "kobodev"
    machine.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", 1024, "--nic2", "hostonly", "--hostonlyadapter1", "vboxnet0" ]
      v.name = "kobo_dev_vm"
    end
  end
end

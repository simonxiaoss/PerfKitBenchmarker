# Copyright 2017 PerfKitBenchmarker Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Contains classes related to managed container services.

For now this just consists of a base cluster class that other container
services will be derived from and a Kubernetes specific variant. This enables
users to run PKB VM based benchmarks on container providers (e.g. Kubernetes)
without pre-provisioning container clusters. In the future, this may be
expanded to support first-class container benchmarks.
"""

import abc

from perfkitbenchmarker import flags
from perfkitbenchmarker import resource

FLAGS = flags.FLAGS
_CLUSTER_REGISTRY = {}

flags.DEFINE_string('kubeconfig', None,
                    'Path to kubeconfig to be used by kubectl')

flags.DEFINE_string('kubectl', 'kubectl',
                    'Path to kubectl tool')


def GetContainerClusterClass(cloud):
  return _CLUSTER_REGISTRY[cloud]


class AutoRegisterContainerClusterMeta(abc.ABCMeta):
  """Metaclass to auto register container cluster classes."""

  def __init__(cls, name, bases, dct):
    if cls.CLOUD:
      _CLUSTER_REGISTRY[cls.CLOUD] = cls


class BaseContainerCluster(resource.BaseResource):
  """A cluster that can be used to schedule containers."""

  __metaclass__ = AutoRegisterContainerClusterMeta
  CLOUD = None

  def __init__(self, spec):
    super(BaseContainerCluster, self).__init__()
    self.name = 'pkb-%s' % FLAGS.run_uri
    self.machine_type = spec.vm_spec.machine_type
    self.zone = spec.vm_spec.zone
    self.num_nodes = spec.vm_count

  def GetMetadata(self):
    """Returns a dictionary of cluster metadata."""
    metadata = {
        'container_cluster_machine_type': self.machine_type,
        'container_cluster_zone': self.zone,
        'container_cluster_size': self.num_nodes,
    }
    return metadata


class KubernetesCluster(BaseContainerCluster):
  """A Kubernetes flavor of Container Cluster."""
  pass

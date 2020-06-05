# Copyright 2019 Google LLC.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""A VcfCaller producing DeepVariantCall and gVCF records.

This module provides a way to call variants with a proposed VCF that contains
candidates to consider.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import flags

from third_party.nucleus.io import vcf
from deeptrio import variant_caller

FLAGS = flags.FLAGS


class VcfCaller(variant_caller.VariantCaller):
  """Call variants and gvcf records from a VCF."""

  def __init__(self,
               options,
               candidates_vcf,
               use_cache_table=True,
               max_cache_coverage=100):
    super(VcfCaller, self).__init__(
        options=options,
        use_cache_table=use_cache_table,
        max_cache_coverage=max_cache_coverage)
    self.vcf_reader = vcf.NativeVcfReader(candidates_vcf).c_reader

  def get_candidates(self, allele_counter, sample_name):
    return self.cpp_variant_caller.calls_from_vcf(allele_counter, sample_name,
                                                  self.vcf_reader)

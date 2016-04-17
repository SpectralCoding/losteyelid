// <copyright file="NodeRepository.cs" company="SpectralCoding.com">
//     Copyright (c) 2016 SpectralCoding
// </copyright>
// <license>
// This file is part of LostEyelid.
// 
// LostEyelid is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// LostEyelid is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with LostEyelid.  If not, see <http://www.gnu.org/licenses/>.
// </license>
// <author>Caesar Kabalan</author>

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebMaster.Models.Node {
	public class NodeRepository : INodeRepository {

		public NodeRepository() {
		}

		public void Add(Node item) {
			throw new NotImplementedException();
		}

		public IEnumerable<Node> GetAll() {
			throw new NotImplementedException();
		}

		public Node Find(String key) {
			throw new NotImplementedException();
		}

		public Node Remove(String key) {
			throw new NotImplementedException();
		}

		public void Update(Node item) {
			throw new NotImplementedException();
		}
	}
}

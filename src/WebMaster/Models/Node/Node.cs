// <copyright file="Node.cs" company="SpectralCoding.com">
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
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Cassandra;
using Cassandra.Mapping.Attributes;
using Cass

namespace WebMaster.Models.Node {
	[Table("lem.nodes")]
	public class Node {
		public String Id { get; set; }
		public String Name { get; set; }
		public String Address { get; set; }
		public DateTime Added { get; set; }
		public Dictionary<String, String> CustomAttributes { get; set; }
	}
}

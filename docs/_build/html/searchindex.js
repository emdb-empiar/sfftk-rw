Search.setIndex({docnames:["adapter","base","converting","core","developing","index","misc","schema","sfftk-rw","toolkit"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,"sphinx.ext.todo":2,sphinx:56},filenames:["adapter.rst","base.rst","converting.rst","core.rst","developing.rst","index.rst","misc.rst","schema.rst","sfftk-rw.rst","toolkit.rst"],objects:{"sfftkrw.core":{parser:[3,0,0,"-"],print_tools:[3,0,0,"-"],utils:[3,0,0,"-"]},"sfftkrw.core.parser":{add_args:[3,1,1,""],parse_args:[3,1,1,""]},"sfftkrw.core.print_tools":{get_printable_ascii_string:[3,1,1,""],print_date:[3,1,1,""],print_static:[3,1,1,""]},"sfftkrw.core.utils":{get_path:[3,1,1,""],rgba_to_hex:[3,1,1,""]},"sfftkrw.schema":{__init__:[7,0,0,"-"],adapter:[0,0,0,"-"],base:[1,0,0,"-"]},"sfftkrw.schema.adapter":{SFFBiologicalAnnotation:[0,2,1,""],SFFBoundingBox:[0,2,1,""],SFFComplexList:[0,2,1,""],SFFComplexesAndMacromolecules:[0,2,1,""],SFFCone:[0,2,1,""],SFFCuboid:[0,2,1,""],SFFCylinder:[0,2,1,""],SFFEllipsoid:[0,2,1,""],SFFExternalReference:[0,2,1,""],SFFExternalReferenceList:[0,2,1,""],SFFGlobalExternalReferenceList:[0,2,1,""],SFFLattice:[0,2,1,""],SFFLatticeList:[0,2,1,""],SFFMacromoleculeList:[0,2,1,""],SFFMesh:[0,2,1,""],SFFMeshList:[0,2,1,""],SFFPolygon:[0,2,1,""],SFFPolygonList:[0,2,1,""],SFFRGBA:[0,2,1,""],SFFSegment:[0,2,1,""],SFFSegmentList:[0,2,1,""],SFFSegmentation:[0,2,1,""],SFFShapePrimitiveList:[0,2,1,""],SFFSoftware:[0,2,1,""],SFFThreeDVolume:[0,2,1,""],SFFTransformList:[0,2,1,""],SFFTransformationMatrix:[0,2,1,""],SFFVertex:[0,2,1,""],SFFVertexList:[0,2,1,""],SFFVolumeIndex:[0,2,1,""],SFFVolumeStructure:[0,2,1,""]},"sfftkrw.schema.adapter.SFFBiologicalAnnotation":{as_hff:[0,3,1,""],description:[0,4,1,""],external_references:[0,4,1,""],from_hff:[0,3,1,""],name:[0,4,1,""],number_of_instances:[0,4,1,""]},"sfftkrw.schema.adapter.SFFBoundingBox":{as_hff:[0,3,1,""],from_hff:[0,3,1,""],xmax:[0,4,1,""],xmin:[0,4,1,""],ymax:[0,4,1,""],ymin:[0,4,1,""],zmax:[0,4,1,""],zmin:[0,4,1,""]},"sfftkrw.schema.adapter.SFFComplexList":{from_hff:[0,3,1,""],ids:[0,4,1,""]},"sfftkrw.schema.adapter.SFFComplexesAndMacromolecules":{as_hff:[0,3,1,""],complexes:[0,4,1,""],from_hff:[0,3,1,""],gds_type:[0,4,1,""],macromolecules:[0,4,1,""]},"sfftkrw.schema.adapter.SFFCone":{bottom_radius:[0,4,1,""],height:[0,4,1,""]},"sfftkrw.schema.adapter.SFFCuboid":{gds_type:[0,4,1,""],x:[0,4,1,""],y:[0,4,1,""],z:[0,4,1,""]},"sfftkrw.schema.adapter.SFFCylinder":{diameter:[0,4,1,""],height:[0,4,1,""]},"sfftkrw.schema.adapter.SFFEllipsoid":{gds_type:[0,4,1,""],x:[0,4,1,""],y:[0,4,1,""],z:[0,4,1,""]},"sfftkrw.schema.adapter.SFFExternalReference":{description:[0,4,1,""],id:[0,4,1,""],label:[0,4,1,""],other_type:[0,4,1,""],type:[0,4,1,""],value:[0,4,1,""]},"sfftkrw.schema.adapter.SFFLattice":{as_hff:[0,3,1,""],data:[0,4,1,""],endianness:[0,4,1,""],from_array:[0,3,1,""],from_bytes:[0,3,1,""],from_hff:[0,3,1,""],id:[0,4,1,""],mode:[0,4,1,""],size:[0,4,1,""],start:[0,4,1,""]},"sfftkrw.schema.adapter.SFFLatticeList":{as_hff:[0,3,1,""],from_hff:[0,3,1,""]},"sfftkrw.schema.adapter.SFFMacromoleculeList":{from_hff:[0,3,1,""],ids:[0,4,1,""]},"sfftkrw.schema.adapter.SFFMesh":{from_hff:[0,3,1,""],num_polygons:[0,3,1,""],num_vertices:[0,3,1,""],polygons:[0,4,1,""],transform_id:[0,4,1,""],vertices:[0,4,1,""]},"sfftkrw.schema.adapter.SFFMeshList":{as_hff:[0,3,1,""],from_hff:[0,3,1,""]},"sfftkrw.schema.adapter.SFFPolygon":{id:[0,4,1,""],vertices:[0,4,1,""]},"sfftkrw.schema.adapter.SFFPolygonList":{from_hff:[0,3,1,""],num_polygons:[0,3,1,""],polygon_ids:[0,3,1,""]},"sfftkrw.schema.adapter.SFFRGBA":{alpha:[0,4,1,""],as_hff:[0,3,1,""],blue:[0,4,1,""],from_hff:[0,3,1,""],green:[0,4,1,""],red:[0,4,1,""]},"sfftkrw.schema.adapter.SFFSegment":{as_hff:[0,3,1,""],as_json:[0,3,1,""],biological_annotation:[0,4,1,""],colour:[0,4,1,""],complexes_and_macromolecules:[0,4,1,""],from_hff:[0,3,1,""],gds_type:[0,4,1,""],id:[0,4,1,""],meshes:[0,4,1,""],parent_id:[0,4,1,""],shapes:[0,4,1,""],volume:[0,4,1,""]},"sfftkrw.schema.adapter.SFFSegmentList":{as_hff:[0,3,1,""],from_hff:[0,3,1,""]},"sfftkrw.schema.adapter.SFFSegmentation":{as_hff:[0,3,1,""],as_json:[0,3,1,""],bounding_box:[0,4,1,""],clear_annotation:[0,3,1,""],copy_annotation:[0,3,1,""],details:[0,4,1,""],from_file:[0,3,1,""],from_hff:[0,3,1,""],from_json:[0,3,1,""],gds_type:[0,4,1,""],global_external_references:[0,4,1,""],lattices:[0,4,1,""],merge_annotation:[0,3,1,""],name:[0,4,1,""],num_global_external_references:[0,3,1,""],primary_descriptor:[0,4,1,""],segments:[0,4,1,""],software:[0,4,1,""],transforms:[0,4,1,""],version:[0,4,1,""]},"sfftkrw.schema.adapter.SFFShapePrimitiveList":{from_hff:[0,3,1,""],num_cones:[0,3,1,""],num_cuboids:[0,3,1,""],num_cylinders:[0,3,1,""],num_ellipsoids:[0,3,1,""]},"sfftkrw.schema.adapter.SFFSoftware":{as_hff:[0,3,1,""],from_hff:[0,3,1,""],name:[0,4,1,""],processing_details:[0,4,1,""],version:[0,4,1,""]},"sfftkrw.schema.adapter.SFFThreeDVolume":{as_hff:[0,3,1,""],from_hff:[0,3,1,""],lattice_id:[0,4,1,""],transform_id:[0,4,1,""],value:[0,4,1,""]},"sfftkrw.schema.adapter.SFFTransformList":{as_hff:[0,3,1,""],from_hff:[0,3,1,""],num_tranformation_matrices:[0,3,1,""]},"sfftkrw.schema.adapter.SFFTransformationMatrix":{cols:[0,4,1,""],data:[0,4,1,""],from_array:[0,3,1,""],gds_type:[0,4,1,""],id:[0,4,1,""],rows:[0,4,1,""],stringify:[0,3,1,""]},"sfftkrw.schema.adapter.SFFVertex":{designation:[0,4,1,""],id:[0,4,1,""],point:[0,3,1,""],x:[0,4,1,""],y:[0,4,1,""],z:[0,4,1,""]},"sfftkrw.schema.adapter.SFFVertexList":{from_hff:[0,3,1,""],num_vertices:[0,3,1,""],vertex_ids:[0,3,1,""]},"sfftkrw.schema.adapter.SFFVolumeStructure":{voxel_count:[0,3,1,""]},"sfftkrw.schema.base":{SFFAttribute:[1,2,1,""],SFFIndexType:[1,2,1,""],SFFListType:[1,2,1,""],SFFType:[1,2,1,""],SFFTypeError:[1,2,1,""]},"sfftkrw.schema.base.SFFIndexType":{from_gds_type:[1,3,1,""],increment_by:[1,4,1,""],index_attr:[1,4,1,""],index_in_super:[1,4,1,""],reset_id:[1,3,1,""],start_at:[1,4,1,""],update_index:[1,3,1,""]},"sfftkrw.schema.base.SFFListType":{append:[1,3,1,""],clear:[1,3,1,""],copy:[1,3,1,""],extend:[1,3,1,""],from_gds_type:[1,3,1,""],get_by_id:[1,3,1,""],get_ids:[1,3,1,""],insert:[1,3,1,""],iter_attr:[1,4,1,""],pop:[1,3,1,""],remove:[1,3,1,""],reverse:[1,3,1,""],sibling_classes:[1,4,1,""]},"sfftkrw.schema.base.SFFType":{"export":[1,3,1,""],from_gds_type:[1,3,1,""],gds_tag_name:[1,4,1,""],gds_type:[1,4,1,""],iter_attr:[1,4,1,""],repr_args:[1,4,1,""],repr_str:[1,4,1,""],repr_string:[1,4,1,""]},sfftkrw:{__init__:[8,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute"},terms:{"0mhussarv19zrbi":4,"0rvx0adhh77cu":4,"0vfurl":4,"0x10bfc66d0":[],"0x10c960dd0":[],"0x10c9c0550":[],"16noz29l300rpesnlfsqncvrivhynoxhnrmv2ebd2oojv4xr5zn1sb6zhzxflghrvv54oihy7end431sw":4,"17rvatvb":4,"191k":[],"1re6uc2fcbfagt8t3zd41dl3fbk3jz33eqp2a":4,"1tt":4,"1tvjpzlaw8nj1mhe70":4,"1u5n182f":4,"1v49scrr2u09":4,"1vp":4,"1wvv3x2vklc":4,"1xm3o":4,"255qhn6l":4,"2etvd3z12fbni":4,"2f2lr6pry4":4,"2rrm":4,"2ur6q1y4":4,"2v3lj1vp6lvblwvmqtbem9rj31qnmrp9f7xjysovkxl40fufj5kyfnkpf":4,"2vg29s9f7ym":4,"2xg5rb9o":4,"2z7m8cvmhi6":4,"381k":[],"399qx":4,"39j4hhv2e":4,"3a3d":4,"3dnerz9yvmd2z06v1v7q8ysgsbbr91stijy65":4,"3ja8":4,"3qs4sa9wj5vg5zz4vi":4,"3vwaf":4,"3x1":[],"3x3":[],"42zvib1na3fwnhcefkfvup33cpsxfk":4,"48h73xjkta2kpvcbmn3kmti":4,"4v28bkdl54vxzv":4,"4wl3uu7et":4,"4x4":[],"4ztjhffun3ze11jzh3voqhx7o5ghnl3no4m57zxvn7yz8548rlfzklzv7gdjmyglndzn2ktc7":4,"52hrtzq2rwz1jw357bs9rtpfnd8zxc1ix3vstbr71obplfdbv1lnnqr1yrdhbev09tzeaw":4,"5cods36t99xrqs3ppv947c8kfdcomp4vvfl8":4,"5idq9us3ve9dxkfn6tjh7o63es6mqmorxesqa695kd9e2wfnrnm5":4,"5lcaqk1ylt48vmtu21ztmennzue0fw6n3vcuwvv2hjmrzsung":4,"5m9iqr7rrpp1p1ldcx":4,"5rcbzffktudzumwxpx3rrff9zyoyb49u3fa9w32xhgv":4,"5thj3bn9hxn65vakax13kttjshxmgnzi":4,"5tjf2uz":4,"5vfxxx4inak5nymysxp":4,"6rfh9l":4,"6vgv6c6dovg9df":4,"7189vnze7":4,"78vvffi655uqzp36wpplpzx1":4,"7tye":4,"7vi3kieusaz":4,"7xdxt":4,"7zpone3o8phqx":4,"81rc199le5sn4gmf1g7ndldpzoqv6vpp7r4udqnxr46x7rn5x5uqr3kp98z3zjrnjsefxdutqxf6zbvjbmtp8l0y81zrst1ris9ux5vb16vbcxsioipp2a":4,"8kemd":4,"8lbvrfh1tpdyw":4,"8m4z7zx752n":4,"8tfw77ubx47g5ur2qrwan70yzlf7xjpzrvnc1cdvk097pml3ez":4,"8u49ohsjpjjevzoun6r1latb32":4,"8x3138dir64vb6vpqswvgvqszjz0lvwzphsf31dpgp4":4,"8x3btprqxf2kj78rz4wx9vxnynqp9zo":4,"8yj6hndwxjzyb":4,"96k":[],"9amnjyw8bhrrbu5t":4,"9b3e3hwh1kit2biro":4,"9vo7lplrrow6vn8fneln1ht7z":4,"9xow3hmg9c2fme37lob":4,"9zodouplodf4zd7bvnm5judt6vbukhcgomxat":4,"9zz41w976eiosvzurja8zmx1ndh3lttrr6wb1pi3z":4,"\u03b2":4,"byte":[0,3],"case":1,"class":[4,7,9],"default":[0,1,2,3,6,9],"export":[1,2,5,9],"final":4,"float":4,"function":[1,2,3,9],"gr\u00fcnewald":9,"import":[0,1,4,9],"int":[0,1,3],"jos\u00e9":9,"long":0,"new":[0,1,4],"null":2,"return":[0,1,3],"short":0,"static":[0,1],"true":[0,1,3],"try":1,"var":1,"while":2,Are:[],For:[1,9],IDs:[0,1],The:[0,1,3,5,6,9],Then:[5,9],There:2,These:4,Use:9,Used:9,Using:5,With:[],__future__:4,__module__:[],__temp_fil:[],__temp_file_ref:[],_arg:[1,3],_bin:[],_check_transformation_matrix_homogen:[],_decod:[],_encod:[],_io:3,_kwarg:1,_local:1,_prep:[],aabbcc:3,abil:[],about:[0,9],abov:[0,1,4],access:0,accident:[],accomplish:[1,2],accord:[],across:0,act:1,action:1,actual:4,ad9aojz0r9ac2fhop:4,adapt:[1,4,7,8,9],add:[3,4],add_arg:3,add_complex:4,add_external_refer:4,add_externalrefer:[],add_lattic:4,add_macromolecul:4,add_mesh:4,add_polygon:4,add_seg:4,add_shap:4,add_to_seg:[],add_transform:4,add_vertex:4,added:4,adding:9,addit:1,addition:[],address:9,affect:[],after:4,agnost:9,ah3kmc9:4,algorithm:[],alia:0,align:[],all:[0,1,2,3,4,6,9],allow:[0,2,9],alongsid:[],alpha:[0,4],alphabet:[],also:[2,9],altern:[],alun:9,am_seg:[],amino:4,amirahxsurfac:[],amirahypersurfacesegment:[],amiramesh:[],amirameshsegment:[],an82vc0ee0pbc4my3xtvb5rqy8irgtgf:4,anaconda:9,ani:[0,1,2,3,6,9],annot:[0,2,9],annotated_sff:4,annotation_onli:0,anoth:0,anyth:[],aozrcs8xv51y5qbyl9nldzdfwtvm9or:4,ap9bjwb:4,apach:9,api:[0,1,4,9],appear:1,append:[1,4],appli:[0,1,2],applic:[4,9],aqd6rbrtlip4gn:4,archiv:0,ardan:9,arg:[1,3],argpars:3,argument:[0,1,2,3,4,6,9],argumentpars:3,arrai:[0,4],arrang:4,articl:9,as_hff:0,as_json:0,as_seg:[],ascii:3,ascii_b:3,ashton:9,aspect:4,assembl:4,associ:[0,4],assum:[0,1,3],atom:4,attempt:[],attribut:[0,1,4,9],augkcv0xrj1r322fqjnxrnvo5lzthyn3njg1ncvrrk0gu9g5ucaqeam7xcdkexixmpflxflu:4,auto:9,auxiliari:[],auxilliari:2,avail:9,background:4,baff5zt:4,bank:9,base64:[0,4],base:[0,7,8],basic:9,bczhduf8145:4,becaus:1,been:[],begin:[0,3],behaviour:1,being:[1,3],below:1,bernard:9,best:[],better:[],between:[2,9],bh71wgz3:4,big:[0,4],bin64:[],binaris:[],binlist2:4,binlist:4,binmap:[],bioann:4,bioinformat:9,biolog:0,biologi:9,biological_annot:[0,4],biologicalannot:0,bj31hsk:4,blah:[],bleed:9,blue:[0,4],bool:[0,3],both:[],bottom:0,bottom_radiu:0,bottomradiu:[0,4],bound:[0,4],bounding_box:[0,4],boundingbox:0,box:[0,4],bp61hn3ozpjphjj:4,bpsuycxxo6eol7ibxhxdusjc:4,brace:1,brandt:9,bridg:9,bridget:9,brief:[0,9],browser:[],build:9,built:[0,1],butcher:9,button:[],byte_seq:0,bzstlzd:4,c6v6:4,c7txmlggowloctznhvyqlw23gnol:4,c7volvfbz8zs7ngwr292plevdx6qakutxpnmgv:4,c8ba6vp5:4,c98y5b5tdl46y42touvsjs4otx17eeybv9aqpem871xvl9vjrnnwyq17:4,call:1,camelcas:0,can:[0,1,2,3,4,9],cannot:[],carazo:9,carragh:9,carri:9,carzaniga:9,cast:1,ccp4:[],cellular:9,central:4,cerevisia:4,certain:0,challeng:9,chang:[1,5,9],channel:[0,3,4],charact:3,check:3,checkout:[5,9],child:4,children:0,chiu:9,choic:[4,9],chosen:[],chromatin:4,chunk:6,cite:9,cl57kwdq:4,classmethod:[0,1],clear:[0,1],clear_annot:0,click:[],close:3,cls:1,code:9,col:[0,4],collect:3,collinson:9,colour:[0,3],column:0,com:9,combin:1,command:[3,4,9],commandlin:3,commenc:[],comment:9,commun:9,comp1:4,comp2:4,comp:4,compact:[],compar:2,complet:[1,4],complex:0,complexes_and_macromolecul:[0,4],complexesandmacromolecul:0,complexid:[],compmacr:4,compon:4,compos:[],compress:2,concaten:[],concentr:3,concert:4,cone:[0,4],conf:[],confer:1,config:2,config_nam:[],config_path:2,config_valu:[],configur:[0,1],conform:[],congruent:[],conserv:4,consid:1,consist:[4,9],constrict:4,construct:0,consult:[4,9],contain:[0,1,2,4],context:9,continu:1,contour:4,contour_level:[],contourlist:[],conveni:[0,1,3],convers:[0,2],convert:[0,1,3,5,9],copi:[0,1],copy_annot:0,copyright:9,core:[2,4,5,6,8,9],corei:9,corner:0,correct:3,correspond:[0,1,9],correspondingli:[],could:[],creat:[0,1,2,5,9],creation:4,crm7dq3ndrefa4mvzvp6tpi:4,crp5vgnbw7nm0g7lu3mxnno:4,cryo:4,csbubz:4,ctp53h1wfo4mbtcy4dm4ed9uoljdsb9r5xn0fac869smew1vpux63v9ktr4dzunhe2v6m2lnni7srnzsl2hvrk0v:4,cu88fgkjoktsimc1nx1tpaqfxqzu6j7:4,cube:[],cuboid:[0,4],current:[1,6,9],custom:[],cylind:[0,4],czxn6o95mfng:4,da9qwn8r0tfa:4,data:[0,1,2,4],dataset:2,date:3,david:9,dbunufkrmhmnlenrw:4,decod:[],decoupl:0,decreas:[],dedic:[],defin:[0,1,3,4],definit:[0,1],deform:4,del:[],del_not:[],delete_from_seg:[],delimit:1,denot:0,depend:[1,9],deriv:0,describ:[0,2,4],descript:[0,2,4,9],descriptor:[4,5,7],design:[0,4,9],detail:[0,1,4,5],detect:9,determin:[0,1,2],dev0:4,dev3:4,develop:5,df6xs7q2urizfqe4yt1zzie9kqetlxuq:4,dh3dwo1x165d2zzd:4,dialogu:[],diamet:[0,4],dict:3,dictionari:[0,1,3],differ:1,dimens:[0,4],dimension:9,directli:1,directori:2,disc:1,discuss:9,disk:4,dismiss:[],displai:[1,2,3],distort:[],djsduu9pdarblr:4,dna:4,doc:9,document:[1,9],doe:[1,3],doing:3,dolor:[2,4],domain:4,done:2,doubl:4,down:[],download:[],drop:2,ds0kcvrbxp79j4xjby:4,due:[],duplex:4,dure:[2,4],dyf:4,e092o0evrord6sr2lu3pv5rt2lu82hn0sprt05b:4,e2b55xzsrtvnmjj17:4,each:[0,1,4],easi:9,easier:0,easili:0,eat4ah7z2mg98dmvx1pm9m9:4,ebi:[4,9],edg:9,edit_in_seg:[],edit_not:[],effect:[],effici:[],either:[0,1,9],ejyn19ko48qorff6:4,ekkdspk1n9cyvi:4,electron:[4,9],elif:9,elimin:[],ellipsoid:[0,4],elmol69svvlkpetn81810k:4,embed:[],embl:9,emd_1014:4,emd_6338:4,emdb:[0,1,5],emdb_sff:[0,1],emdb_stat:9,emma:9,emmkrfnsbe6ctcyp71ktq2zfw5c5utx:4,empiar:9,empti:[0,1],enabl:[1,2],encapsul:0,encod:[0,3,4],end:3,endian:[0,4],ensur:[2,3],entiti:0,entri:4,environ:9,eqt:4,equal:[],equival:2,erp7xt7pfs9r3xth5cwky583fdt6:4,error:[1,2],etc:0,eukaryot:4,european:9,even:2,eventu:[],everi:[1,4],exampl:[0,1,9],except:[1,2,9],exclud:[1,2],exclus:9,exist:[0,9],exit:[2,6,9],exlus:[],expect:[],experi:9,explicit:[],express:9,ext:[],extend:[1,4,9],extens:[1,2,4],extern:0,external_refer:[0,4],externalrefer:[0,4],externalreferenceid:[],extra:[],extract:0,extref:4,f1xxq1gs0euex3lrd:4,f2r:4,factor:4,fail:2,fallback:[],fals:[0,1,2,3,6],far:4,fashion:4,featur:4,fefxxb1:4,fewer:9,fiction:1,field:[2,4],file1:[],file2:[],file3:[],file:[0,1,3,5,9],file_:[],file_bin:[],file_doubl:[],file_prep:[],file_transform:[],file_tx:[],filenam:1,filetyp:2,fill:1,filter:[],find:[],first:[0,1,3,4],fit:4,flag:[],flank:4,float32:[0,4],float64:0,follow:[1,2,9],fom:[],form:4,format:[0,1,3,4,5,6,9],found:1,four:4,fq08b0otavjfefzw:4,fqcyedisnrdhnndcubmvgwys3m:4,fraction:[],free:[0,9],freeli:[],frhlj:4,fri:[],from:[0,1,2,3,4,9],from_arrai:0,from_byt:0,from_fil:[0,2,6,9],from_gds_typ:1,from_hff:0,from_id:0,from_json:0,frtxvyy1z2nm1pcep7rivlqflepx2zo22vvok1x3weqx6vtxi76bvjfhi0fbg56trwpexpmvzvy59zhfkrrxl:4,fulfil:0,full:[6,9],fzr9nu65l1j:4,g0blivxud:4,gate:4,gault:9,gds_tag_nam:[0,1],gds_type:[0,1],gener:[0,1,4],geometr:[0,2],get:[0,1,3,5],get_by_id:[1,4],get_data:[],get_id:[1,4],get_path:3,get_printable_ascii_str:3,git:9,github:9,given:[0,1,3],global:0,global_external_refer:0,grant:9,graphic:[],greater:[],green:[0,4],group:[0,9],guarante:1,guid:[2,9],h54qbtrv5r15oxgv51qjledah:4,h5py:0,hairpin:4,handl:[0,1,4,9],handle_convert:3,handler:3,has:[0,1,4],hashabl:3,have:[1,4,9],hdf5:[0,1,2,4,9],header:4,heavi:3,hecksel:9,height:[0,4],helicas:4,help:[1,2,3,6,9],helper:[],henc:[],henderson:9,here:[0,4],heterohexamer:4,hex:3,hexam:4,heymann:9,hff:[0,1,2,4,9],hff_data:0,hill:9,hit:[],hns6c:4,hoc:[],hold:[],homogen:[],hope:[],host:0,houf3tnsobyw16tq3bpzn:4,how:[0,1,2,4,9],howev:[1,9],html:9,http:[4,9],hundr:[],ideal:2,ident:4,identifi:[],ids:0,ieof:[],ignor:1,ihg7y1qfphr:4,imag:[],imat:[],imod:6,imodmesh:[],imodsegment:[],implement:0,impli:0,improv:9,inact:4,incl_dat:3,includ:[1,3],incorpor:[],increment:1,increment_bi:1,indent:0,indent_width:0,independ:4,index:[0,1,4,5],index_attr:1,index_in_sup:1,indic:0,individu:[1,2,4],infer:[0,4],infil:[],inform:[0,2,4],inherit:0,input:[],insert:[1,2],insid:1,inspector:[],inst:1,instal:[],instanc:[0,1],instanti:0,instead:3,institut:9,int16:0,int32:0,int64:0,int8:0,integ:[],integr:[0,4,9],interact:4,interdigit:4,interest:[],interfac:4,interior:4,interv:[3,4],interven:4,introduct:5,invok:[],ip1p78n81lp:4,ipsum:[2,4],iri1:[],iri2:[],iri:0,iroqmvnvmsot3qo:4,irviu3uc:4,item:[1,3],iter:[0,1,3],iter_attr:1,its:[1,4],iu21fvqi7ehh:4,jan:[],jcw:4,jegvtoun8yhpl77l90r5v2v:4,jensen:9,jm30wq:4,join:4,jrx5lntwz1n:4,jsf:4,json:[0,1,2,4,9],json_fil:0,k0cyhfwrrwne5p7:4,kai:9,kei:[0,3],keyword:[0,1,3],kind:[],kink:4,klass:1,know:[],kseqhpfmg8ngt85mztal:4,kvvjvdy:4,kwarg:[1,3],kx1jvvxzjvrz4o8qa9xbc3rizwx3pefoosupqmwal7kj2ttzi2lc23yn5i2vs3jk:4,l37bb:4,l43a:4,l5mxed:4,label:[0,4],lack:4,larg:2,larger:[],last:1,lattic:[0,4],lattice2:4,lattice_id:0,latticeid:[0,4],launch:[],lbxlr6vlvocn2jdrvesvgs9c7:4,lczfnfzef5cplbxvrhfvyk7x65p:4,lead:[],least:[],left:[],len:[1,4],length:[0,1,4],level:[0,1,2,4],lf3ddvahh9k9en:4,lib:3,licens:4,lift:3,like:[1,4],line:[3,4,9],linux:2,list:[0,1,3,6],listinfo:9,listserv:9,liter:1,littl:[0,4],lj33q19be:4,lj6y:4,loa77xzcxry3oal87j9ofzb3hmp8mt8rb:4,load:1,loc43md15ytz6xz2rxv3kexwyugm:4,local:[],locat:[1,4],look:[4,5,9],lorem:[2,4],lossless:2,luci:9,lurfyfgxs1sd73bqwn:4,m48z39iyfj2jvdiz7gwtpsv2byk78dt5ws52fl:4,m9elknqc2afxiylxz98uv:4,macr1:4,macr2:4,macr:4,macromolecul:0,macromolecular:9,macromoleculeid:[],macromoleculesandcomplexestyp:0,magic:1,mai:[0,9],mailman:9,main:[0,1,2,4,6],mainli:4,mainten:4,make:[0,2,4],manag:[1,9],mandatori:2,mani:2,manner:[],map:[2,4],map_seg:[],mapsegment:[],mar:[],march:[],maria:9,mark:[],mask:[],mask_valu:[],matric:[],matrix:[0,4],maxim:3,maximum:0,mbnw2d7sa1ktc2vvdnzv:4,mbv199ioj:4,mcm2:4,mcm5:4,mcm7:4,mean:9,mechan:4,melt:4,memori:[],menu:[],merg:0,merge_annot:0,mesh:[0,2],meshlist:[0,2,4],messag:[1,2,6,9],metadata:[5,9],method:[0,4],mfde2by6zr50vl:4,mg68z371sf6shzef14d73:4,microscopi:[4,9],might:[],minichromosom:4,miniconda:9,minimum:0,minx:[],miscellan:[4,5,8],mixin:[],mlq:4,mod:6,mod_seg:[],mode:[0,3,4],model:[0,2,6],modifi:3,modread:[],modul:[0,1,5,8],molecular:9,more:0,most:[0,1],mostli:[],mpy41w:4,mql:4,mrc:2,much:[],multi:2,multifil:[],multipl:[0,2],must:[],mvcnz1irpnu2l:4,my_arg:3,my_output:[],n2u0cqk60z7vml:4,n69ve:4,n9phit:4,naiv:[],name:[0,1,3,4,9],namespac:3,narrow:4,natur:9,navig:5,ncbitaxon:4,ncbitaxon_559292:4,ndarrai:0,necessari:[],need:[1,4],newlin:3,newmodel:[],next:[1,4],njhlvfzv3nq3wp81omvdnvbxhbcbpf:4,nnylfbek9xtj4q0ylp5nvuenm0gu20sspnlmzc1p:4,no_polygon:4,no_vertic:4,non:[0,3],none:[0,1,2,4],normal:[0,4],normalis:[3,4],note:[0,4,6],notic:1,now:[0,1,4],npvq0ffqudg42tj3lukrtqonnvnonv9aj3nx:4,nsxxczapgl98rhe12zrdz7ogznfgpm:4,num_con:0,num_cuboid:0,num_cylind:0,num_ellipsoid:0,num_global_external_refer:0,num_polygon:0,num_tranformation_matric:0,num_vertic:0,number:[0,3],number_of_inst:0,number_ofinst:4,numberofinst:4,numpi:[0,4],nwd7xvmzm:4,nxephv9wtd:4,o3vrm0onefy7mttz:4,obj:1,object:[0,1,2,3,5],objt:[],obo:4,obo_id1:[],obo_id2:[],obolibrari:4,obtain:0,occupi:[],occur:1,occurr:1,oct:[],offset:4,often:[],onc:4,one:[0,1,2,4,6,9],onli:[0,1,2,6,9],ontolog:0,ontology1:[],ontology2:[],opac:0,open:[0,9],oper:[1,5],opjhbr7x3jsj7lppzbc7i:4,option:[0,2,6,9],order:0,ordin:0,org:4,origin:[2,4],other:[0,1,2,4,5,9],other_seg:0,other_typ:0,othertyp:[0,4],otherwis:[1,2],ought:[],our:4,out:9,outlin:[],output:[0,1,4,5,6,9],outsid:[],over:[0,1],overcrowd:3,overwrit:[1,3],ovlc6:4,oxnz6mof8wmfcanxdq3fg0c5ei:4,p61x6uxhud3pf:4,packag:[4,5,9],page:5,pair:[1,4],param:[],paramet:[0,1,3],paraview:[],parent:[0,1],parent_group:0,parent_id:[0,4],parentid:4,pars:3,parse_arg:3,parser:8,part:[],particular:[],partit:[],pass:[1,2],passagewai:4,path:[3,4],patwardhan:9,pdb:4,pdbe:[4,9],per:1,perform:[2,9],persist:[],perus:9,pfex3f3m:4,phase:4,physic:[],pib:4,pid:0,pip:9,pipelin:[],pipenv:9,pixel:[],pjexmfzxstysrgsq:4,pkorir:[4,9],place:[1,4],plai:[],pleas:[4,9],plu:[],point:[0,1,4],polygon:[0,4],polygon_id:0,polygonlist:0,pop:1,popul:[1,2],posit:[0,2,3,6],possibl:2,powerfulli:[],pqn88rz:4,pr_p38132:4,pre:[],preced:[],prefix:3,prep:[],prepar:9,preparatori:[],present:[],prevent:[],previous:2,primari:[4,5],primarili:2,primary_descriptor:[0,2,4],primarydescriptor:[0,2],primit:[0,2],print:[1,2,4,8],print_dat:3,print_funct:4,print_stat:3,print_str:3,printabl:3,prioriti:[],prioritis:[],process:[0,2],processing_detail:0,processingdetail:[0,1,4,9],produc:[0,1],program:2,programmeu:0,progress:3,properli:3,properti:0,provid:[0,1,2,4,9],ptmahmmt:4,publish:9,purifi:4,purl:4,put:[1,2],pw59jtx6285fs9n1a4z19azwnnmo365qxtxr:4,pycharmproject:4,pyenv:9,python2:[],python:[4,9],pzwp452d8p9u3znv9mvfhvmsa4fniwcq33mydj3vvw55w9xubf:4,q59oa:4,qi9fnfj8vp5md8pm4sgem1rqxqz23poo8loe0p:4,qk5pll2i9izvek59agfd9zyw:4,qtnny55ezoxhdtdvy1fvmix5ud:4,qtz:4,question:9,qzr3kndusrx:4,r5lt:4,r6hhqm:4,r7hv9a38:4,r8my9a1fyu49p71qbds0unmtensxq3:4,r9pxirxnf3vsfdo35es97hnutd86nxtp6m:4,radiu:0,raffaella:9,rais:[1,2],randint:4,random:4,random_colour:0,rang:4,rbvz75rf:4,read:[1,5],reader:6,real:[],rec:2,receiv:[1,9],recommend:9,red:[0,4],redefin:3,reduc:[],redunt:2,refer:[0,1,3],referenc:[0,1],region:[],regul:4,reinforc:4,reinstat:2,rel:[2,4],relat:[],releas:9,relev:9,reli:3,rememb:[],remov:1,render:0,replac:[],replic:4,report:4,repr_arg:1,repr_str:[0,1],repres:[0,4],represent:[0,1,4],requir:[0,1,4],reset:1,reset_id:1,respect:[0,4,9],respons:[],result:[2,9],retriev:1,reus:3,revers:1,rg7fz:4,rgb:3,rgba:[0,3,4],rgba_to_hex:3,rhxzqytw:4,richard:9,right:4,rigid:[],ring:4,robert:9,root:[0,4],rotat:[],roughli:[],row:[0,4],rqemsdgk5sev98pa8b1v7g6exvhxvx:4,rtype:0,run:[2,5,9],rv6l97txvwqblod8r9nmns8uwvp2m3jnhrbcihokm6t:4,ry0a9ypfbh1ib:4,rz5y17:4,s1ecd:4,s1nkgv5sw4xno9nm8:4,s288c:4,s3n8:4,s5wdjdccvro599dmnl:4,s759fm388tde1md9k:4,s7y:4,s8z:4,saccharomyc:4,sai:4,same:[0,2],sampl:1,san:4,saniti:3,sarah:9,save:[],sbz1:4,schema:[4,5,6,8,9],scheme:[],scratch:[4,9],screen:3,search:[3,5],second:4,section:[0,4],see:9,seem:[],seg:[0,2,4,9],seg_fn:4,seg_seg:[],segger:4,seggersegment:[],segment:[0,1,2,5,9],segmentation_da:9,segmentation_da_doc:9,segmentationa:[],segmentlist:0,segmenttyp:0,segread:[],segtran:9,select:[],sep:2,separ:0,sequenc:[0,6],sequenti:[],set:[0,1],sete:2,sever:[0,1,3,4],sf853zezf9:4,sff:[0,1,3,5,6],sff_seg:0,sff_type:[0,1],sffattribut:[0,7],sffbiologicalannot:[4,7],sffboundingbox:[4,7],sffcomplex:[1,4],sffcomplexesandmacromolecul:[4,7],sffcomplexlist:7,sffcone:[1,4,7],sffcuboid:[1,4,7],sffcylind:[1,4,7],sffellipsoid:[1,4,7],sffexternalrefer:[4,7],sffexternalreferencelist:7,sffglobalexternalrefer:0,sffglobalexternalreferencelist:7,sffindextyp:[0,7],sffitem:1,sfflattic:[4,7],sfflatticelist:[4,7],sfflisttyp:[0,7],sffmacromolecul:[1,4],sffmacromoleculelist:7,sffmesh:[4,7],sffmeshlist:[4,7],sffpolygon:[4,7],sffpolygonlist:[4,7],sffrgba:[4,7],sffsegment:[1,2,4,7,9],sffsegmentlist:[1,4,7],sffshape:[0,1],sffshapeprimitivelist:[1,4,7],sffsoftwar:[0,1,4,9],sfftest:1,sffthreedvolum:[4,7],sfftk:[0,2],sfftkrw:[3,4,7,8,9],sfftransformationmatrix:[4,7],sfftransformlist:[4,7],sfftype:[0,4,7],sfftypeerror:7,sffvertex:[4,7],sffvertexlist:[4,7],sffvolum:0,sffvolumeindex:[4,7],sffvolumestructur:[4,7],shallow:1,shape:[0,1,2],shapeprimitivelist:[0,2],share:[],shell:2,ship:2,shlex:3,should:[0,1,2,4,9],show:[2,4,6,9],sibl:[],sibling_class:1,sif9dcarhzyznnvzin7n:4,signifi:1,similar:[],similarli:2,simplenot:[],simplest:[],simpli:9,simplifi:[4,9],singl:[0,1,2,4],sit:0,site:[],size:[0,4],smooth_decim:[],sns4h9nxoezmwd:4,softwar:[1,4,7,9],some:[1,4],someth:4,sort:0,sort_kei:0,sourc:[],space:0,special:1,specif:9,specifi:[0,1,3,4,5,9],staff:[],standard:[],start:[0,1,4,5],start_at:1,state:2,statist:[],statu:2,stderr:[3,4],stdout:3,step:4,stereolithographi:[],stl:2,stl_seg:[],stlsegment:[],store:[],str:[0,1,3],straightforward:4,stream:3,strictli:4,string:[0,1,3,9],stringifi:0,structur:[0,3,4,9],stuff:3,su8zhnj1f5kjeuqn6pjbb:4,sub:[],subclass:1,subcommand:[],subunit:4,suffix:0,suggest:[4,9],summari:[6,9],sunqzn:4,superclass:[],suppli:[],support:9,supported_format:[],sure:4,surf:[],surf_seg:[],surfac:[0,4],sv9ld1o75u9:4,sw5zjt7ot31odypz7zewgehz4uhzffmt5:4,sxvhxplmptdfdzqce:4,sys:[3,4],t8boxxxc1vfi:4,tabl:[],tag:[1,2],take:[0,2],target:[],task:2,tba:[],tdfdi0f:4,temp:[],temporari:2,tend:[],term:9,termin:[2,4],test:[1,5,9],test_data:4,test_data_path:4,text:[0,1],textiowrapp:3,textual:9,tgx19lrj6x91k:4,than:[],the_arg:3,thei:[1,4],them:[2,4],themselv:[],therebi:[],therefor:[0,1],thi:[0,1,2,3,4,6,9],third:[],this_pars:3,those:0,thousand:[],three:[0,2,9],threedvolum:[0,2,4],threshold:[],through:5,thu:[],tightli:4,tilt:4,time:[],tkfaqttugfam:4,tnf53svzssievj:4,to_id:0,togeth:1,tool:[6,9],toolkit:[4,5],top:2,transfer:[],transform:[0,4],transform_id:0,transformationmatrixtyp:0,transformid:[0,4],transformlist:0,translat:[],treat:[1,2,3],tree:[],tri:[],truncat:[],tue:2,tupl:[1,3,4],twice:[],twist:4,two:[0,1,2,4],twvnzve286jtfuvmmbu72wxyz33kshcogr9m7v11tfxrlrhpofngl7evixxzvl2t:4,tx_file:[],type:[0,1,3,4,9],type_:[],typic:[1,2],u96v9v:4,ubc7hp7bx2wtp1b1e7luo:4,udzx2z:4,uint16:0,uint32:[0,4],uint64:0,uint8:0,under:9,underli:4,underscore_cas:0,unicod:[0,3],unit:[5,9],unittest:4,unmodifi:[],unusu:4,updat:[],update_count:[],update_index:1,upon:[0,1],urae8pzvqyzd2tahwtfgn95frlhvq7:4,url:0,usabl:0,usag:[2,3,6,9],use:[0,2],use_shlex:3,used:[0,1,2,4,9],useful:[3,4],user:[0,1,2,4],uses:0,using:[0,1,2,3,4,9],usr:[],utf:3,util:[4,8,9],utilis:[],utlzruvfp:4,utr47bhh34fnfxcytu3ai51znfxy0xxrqn:4,uucsw29f1tkpezz870vv7zn6y75ry8szu2pvxj4q7qqhn7cet1:4,uvntc:4,uz5xqcmuplsoddzvrbwdrnboj9jr3rgudem5ruclmdffdbzw5y41j5xm:4,v9f7vnqbjz30xvbggfzzmrycazdz5l5:4,val:[],valid:[0,1,2],valu:[0,1,2,3,4],valueerror:2,variabl:[1,3],variou:9,vb9xvnufo1c4dmvcnihbewfdc2wg:4,verbos:[5,6],version:[0,1,4,5,9],vertex:[0,4],vertex_id:[0,4],vertexlist:0,vertic:[0,4],vg9o7jxd5qxz7tvoxs4z45jxu:4,vid:0,view:[1,5],virtual:9,virtualenv:9,vjnwvnnf9l8pltcn9ny:4,vndxlk:4,vol1_valu:4,vol2_valu:4,volum:[0,2],voxel:[0,4],voxel_count:0,vs8:4,vtcxtpffqneskd1ujqyg1wa18a29xdneg7wesmakv9avzla:4,vuwlaohjf:4,w555v25izor4mdd:4,w7usbyfpewl4qz4zm2r3ckz4wx28:4,wah:9,wai:[0,1,2,3,5],want:[],watersh:[],wb0:4,wbpobz:4,wctypn73bnzd5g9na:4,wczy05g:4,welcom:9,well:[],what:1,when:[1,2,9],whenev:[1,9],where:[0,1,6],wherebi:[],whether:[0,1,3],which:[0,1,4,9],whole:0,whose:2,width:0,within:[],without:[1,3],wiu13djv7:4,wlvy:4,work:[0,1,2,4,6,9],world:9,would:[],writabl:[],write:[0,3,4,5],written:[],wsj7xvjgph1dp7vr9sxzyjfi:4,www:4,wwwdev:9,wzpd9ziz6df9vvr:4,x1mznsrr9pkz4re2wofqpndsvbcxc2rlf2ur:4,xdb3pxnm8:4,xfv58wnv5:4,xfzfctyjnw48qp2lohogpmn:4,xhromcvvfisl1yrxh5f4di:4,xikfywd7z3gpne6uzu3gzl9vantnel2pke:4,xlmg3v1r1xlvqpv9iou7apfivs6s17h:4,xmax:[0,4],xmd9n5c:4,xmg9pvm3ljs754ct1w2xmwfp6pngz11ay33pdc8vqcf:4,xmin:[0,4],xml:[0,1,2,4,9],xrang:4,xszqpv2vvwqw6sljax5mef26tqc3pb2wxpt2xup1ht8wgo21mz33iypujjrmhvlup1wwxc2sp18txe73:4,xxpdtezi7pkz1tjvzozwf1:4,xz15c8b:4,y6ps1wedhalj:4,yadz1jf8bbg8n9:4,ybx46z2a:4,yd0z88r93oan33v2f:4,ydaihz9mt:4,yeast:4,yj2:4,ymax:[0,4],ymewtz2hntdwd9tlzylxhvlb2agzli:4,ymin:[0,4],you:9,your:[5,9],yqheul9hr1sztlwdsye3vleazoqb6qt:4,ywsthv:4,z9a3d4vv:4,zejewsaj289ywx8uulij05q670nnp7sby1dx6lr5nv2g22ynniqf3d:4,zero:[],zfyh9pwn6jhryk8u1z1ltvuull9m4r:4,zip:0,zk3js2tedufz7fon8nwe68zvr629:4,zmax:[0,4],zmduh8su:4,zmin:[0,4],zqf1thgjx86x5qz1vtnxq1n78nhnlr3uz4mda3e9axmdgsn6rv1hn3lcp:4,zru5jx3vimyf8vljc:4,zspfdfdbz3xh6hlxhjt6s8zxxlj9c:4,zve:4,zwtqlv33j65ndmruqacaz47p8tt9po83r64zpuzwgfwpnnphfyplu8vrsc3vz:4,zxzht:4,zzxoalh9aa80n:4},titles:["sfftkrw.schema.adapter","sfftkrw.schema.base","Converting Files To EMDB-SFF","sfftk.core package","Developing with <code class=\"docutils literal notranslate\"><span class=\"pre\">sfftk-rw</span></code>","Welcome to <code class=\"docutils literal notranslate\"><span class=\"pre\">sfftk-rw</span></code>\u2019s documentation!","Miscellaneous Operations Using sfftk-rw","sfftk.schema package","sfftk packages","EMDB-SFF Read/Write Toolkit (<code class=\"docutils literal notranslate\"><span class=\"pre\">sfftk-rw</span></code>)"],titleterms:{"byte":[],"class":[0,1],"default":[],"export":4,"public":9,Adding:4,Are:[],IDs:4,The:[2,4],Use:[],Using:6,adapt:0,all:[],amira:[],amiramesh:[],annot:4,applic:[],avail:[],base:1,bin:[],biolog:4,ccp4:[],chang:2,chunk:[],clear:[],colour:4,command:[],complex:4,configur:[],contact:9,content:[2,4,5,6,9],contour:[],convert:2,core:3,creat:4,data:9,delet:[],descriptor:[1,2],detail:2,develop:[4,9],document:5,edit:[],emdb:[2,4,9],extern:4,file:[2,4,6],flag:2,format:2,get:[4,9],hypersurfac:[],imod:[],indic:5,infix:[],input:[],instal:9,interconvers:[2,9],interfac:9,introduct:[2,4,9],iter:4,level:[],licens:9,list:4,macromolecul:4,map:[],mask:[],mesh:4,metadata:[4,6],miscellan:[3,6],mod:[],model:9,modul:3,multifil:[],navig:4,negat:[],note:[],number:[],object:4,obtain:9,onli:[],oper:[2,6],option:[],origin:[],output:2,overwrit:[],packag:[3,7,8],parent:4,parser:3,path:2,per:[],prep:[],primari:2,print:3,print_tool:3,pypi:9,quick:2,read:[4,9],reduct:[],refer:4,run:6,schema:[0,1,7],seg:[],segger:[],segment:4,set:[2,4],sff:[2,4,9],sffattribut:1,sffbiologicalannot:0,sffboundingbox:0,sffcomplex:[],sffcomplexesandmacromolecul:0,sffcomplexlist:0,sffcone:0,sffcuboid:0,sffcylind:0,sffellipsoid:0,sffexternalrefer:0,sffexternalreferencelist:0,sffglobalexternalrefer:[],sffglobalexternalreferencelist:0,sffindextyp:1,sfflattic:0,sfflatticelist:0,sfflisttyp:1,sffmacromolecul:[],sffmacromoleculelist:0,sffmesh:0,sffmeshlist:0,sffpolygon:0,sffpolygonlist:0,sffrgba:0,sffsegment:0,sffsegmentlist:0,sffshapeprimitivelist:0,sffthreedvolum:0,sfftk:[3,4,5,6,7,8,9],sfftkrw:[0,1],sfftransformationmatrix:0,sfftransformlist:0,sfftype:1,sfftypeerror:1,sffvertex:0,sffvertexlist:0,sffvolumeindex:0,sffvolumestructur:0,shape:4,show:[],singl:[],softwar:0,sourc:9,specif:[],specifi:2,start:[2,9],stl:[],store:[],surf:[],synopsi:2,tabl:5,test:6,through:4,todo:0,toolkit:9,transform:[],truncat:[],unit:6,user:9,util:3,valu:[],verbos:2,version:6,view:[4,6,9],volum:4,voxel:[],wai:4,welcom:5,where:[],work:[],write:9,xml:[],your:4}})
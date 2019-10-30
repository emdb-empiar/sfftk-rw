Search.setIndex({docnames:["converting","core","developing","index","misc","schema","sfftk-rw","toolkit"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,"sphinx.ext.todo":2,sphinx:56},filenames:["converting.rst","core.rst","developing.rst","index.rst","misc.rst","schema.rst","sfftk-rw.rst","toolkit.rst"],objects:{"sfftkrw.core":{parser:[1,0,0,"-"],print_tools:[1,0,0,"-"],utils:[1,0,0,"-"]},"sfftkrw.core.parser":{add_args:[1,1,1,""],parse_args:[1,1,1,""]},"sfftkrw.core.print_tools":{get_printable_ascii_string:[1,1,1,""],print_date:[1,1,1,""],print_static:[1,1,1,""]},"sfftkrw.core.utils":{get_path:[1,1,1,""],rgba_to_hex:[1,1,1,""]},"sfftkrw.schema":{adapter:[5,0,0,"-"],base:[5,0,0,"-"]},"sfftkrw.schema.adapter":{SFFBiologicalAnnotation:[5,2,1,""],SFFBoundingBox:[5,2,1,""],SFFComplexes:[5,2,1,""],SFFComplexesAndMacromolecules:[5,2,1,""],SFFCone:[5,2,1,""],SFFCuboid:[5,2,1,""],SFFCylinder:[5,2,1,""],SFFEllipsoid:[5,2,1,""],SFFExternalReference:[5,2,1,""],SFFExternalReferences:[5,2,1,""],SFFGlobalExternalReferences:[5,2,1,""],SFFLattice:[5,2,1,""],SFFLatticeList:[5,2,1,""],SFFMacromolecules:[5,2,1,""],SFFMesh:[5,2,1,""],SFFMeshList:[5,2,1,""],SFFPolygon:[5,2,1,""],SFFPolygonList:[5,2,1,""],SFFRGBA:[5,2,1,""],SFFSegment:[5,2,1,""],SFFSegmentList:[5,2,1,""],SFFSegmentation:[5,2,1,""],SFFShape:[5,2,1,""],SFFShapePrimitiveList:[5,2,1,""],SFFSoftware:[5,2,1,""],SFFThreeDVolume:[5,2,1,""],SFFTransformList:[5,2,1,""],SFFTransformationMatrix:[5,2,1,""],SFFVertex:[5,2,1,""],SFFVertexList:[5,2,1,""],SFFVolume:[5,2,1,""],SFFVolumeIndex:[5,2,1,""],SFFVolumeStructure:[5,2,1,""]},"sfftkrw.schema.adapter.SFFBiologicalAnnotation":{as_hff:[5,3,1,""],description:[5,4,1,""],external_references:[5,4,1,""],from_hff:[5,3,1,""],name:[5,4,1,""],number_of_instances:[5,4,1,""]},"sfftkrw.schema.adapter.SFFBoundingBox":{as_hff:[5,3,1,""],from_hff:[5,3,1,""],xmax:[5,4,1,""],xmin:[5,4,1,""],ymax:[5,4,1,""],ymin:[5,4,1,""],zmax:[5,4,1,""],zmin:[5,4,1,""]},"sfftkrw.schema.adapter.SFFComplexes":{from_hff:[5,3,1,""],ids:[5,4,1,""]},"sfftkrw.schema.adapter.SFFComplexesAndMacromolecules":{as_hff:[5,3,1,""],complexes:[5,4,1,""],from_hff:[5,3,1,""],gds_type:[5,4,1,""],macromolecules:[5,4,1,""]},"sfftkrw.schema.adapter.SFFCone":{bottom_radius:[5,4,1,""],height:[5,4,1,""]},"sfftkrw.schema.adapter.SFFCuboid":{gds_type:[5,4,1,""],x:[5,4,1,""],y:[5,4,1,""],z:[5,4,1,""]},"sfftkrw.schema.adapter.SFFCylinder":{diameter:[5,4,1,""],height:[5,4,1,""]},"sfftkrw.schema.adapter.SFFEllipsoid":{gds_type:[5,4,1,""],x:[5,4,1,""],y:[5,4,1,""],z:[5,4,1,""]},"sfftkrw.schema.adapter.SFFExternalReference":{description:[5,4,1,""],id:[5,4,1,""],label:[5,4,1,""],other_type:[5,4,1,""],type:[5,4,1,""],value:[5,4,1,""]},"sfftkrw.schema.adapter.SFFLattice":{as_hff:[5,3,1,""],data:[5,4,1,""],endianness:[5,4,1,""],from_array:[5,3,1,""],from_bytes:[5,3,1,""],from_hff:[5,3,1,""],id:[5,4,1,""],mode:[5,4,1,""],size:[5,4,1,""],start:[5,4,1,""]},"sfftkrw.schema.adapter.SFFLatticeList":{as_hff:[5,3,1,""],from_hff:[5,3,1,""]},"sfftkrw.schema.adapter.SFFMacromolecules":{from_hff:[5,3,1,""],ids:[5,4,1,""]},"sfftkrw.schema.adapter.SFFMesh":{from_hff:[5,3,1,""],num_polygons:[5,3,1,""],num_vertices:[5,3,1,""],polygons:[5,4,1,""],transform_id:[5,4,1,""],vertices:[5,4,1,""]},"sfftkrw.schema.adapter.SFFMeshList":{as_hff:[5,3,1,""],from_hff:[5,3,1,""]},"sfftkrw.schema.adapter.SFFPolygon":{id:[5,4,1,""],vertices:[5,4,1,""]},"sfftkrw.schema.adapter.SFFPolygonList":{from_hff:[5,3,1,""],num_polygons:[5,3,1,""],polygon_ids:[5,3,1,""]},"sfftkrw.schema.adapter.SFFRGBA":{alpha:[5,4,1,""],as_hff:[5,3,1,""],blue:[5,4,1,""],from_hff:[5,3,1,""],green:[5,4,1,""],red:[5,4,1,""]},"sfftkrw.schema.adapter.SFFSegment":{as_hff:[5,3,1,""],as_json:[5,3,1,""],biological_annotation:[5,4,1,""],colour:[5,4,1,""],complexes_and_macromolecules:[5,4,1,""],from_hff:[5,3,1,""],gds_type:[5,4,1,""],id:[5,4,1,""],meshes:[5,4,1,""],parent_id:[5,4,1,""],shapes:[5,4,1,""],volume:[5,4,1,""]},"sfftkrw.schema.adapter.SFFSegmentList":{as_hff:[5,3,1,""],from_hff:[5,3,1,""]},"sfftkrw.schema.adapter.SFFSegmentation":{as_hff:[5,3,1,""],as_json:[5,3,1,""],bounding_box:[5,4,1,""],clear_annotation:[5,3,1,""],copy_annotation:[5,3,1,""],details:[5,4,1,""],from_file:[5,3,1,""],from_hff:[5,3,1,""],from_json:[5,3,1,""],gds_type:[5,4,1,""],global_external_references:[5,4,1,""],lattices:[5,4,1,""],merge_annotation:[5,3,1,""],name:[5,4,1,""],num_global_external_references:[5,3,1,""],primary_descriptor:[5,4,1,""],segments:[5,4,1,""],software:[5,4,1,""],transforms:[5,4,1,""],version:[5,4,1,""]},"sfftkrw.schema.adapter.SFFShape":{attribute:[5,4,1,""],id:[5,4,1,""],transform_id:[5,4,1,""],update_counter:[5,3,1,""]},"sfftkrw.schema.adapter.SFFShapePrimitiveList":{from_hff:[5,3,1,""],num_cones:[5,3,1,""],num_cuboids:[5,3,1,""],num_cylinders:[5,3,1,""],num_ellipsoids:[5,3,1,""]},"sfftkrw.schema.adapter.SFFSoftware":{as_hff:[5,3,1,""],from_hff:[5,3,1,""],name:[5,4,1,""],processing_details:[5,4,1,""],version:[5,4,1,""]},"sfftkrw.schema.adapter.SFFThreeDVolume":{as_hff:[5,3,1,""],from_hff:[5,3,1,""],lattice_id:[5,4,1,""],transform_id:[5,4,1,""],value:[5,4,1,""]},"sfftkrw.schema.adapter.SFFTransformList":{as_hff:[5,3,1,""],from_hff:[5,3,1,""],num_tranformation_matrices:[5,3,1,""]},"sfftkrw.schema.adapter.SFFTransformationMatrix":{cols:[5,4,1,""],data:[5,4,1,""],from_array:[5,3,1,""],gds_type:[5,4,1,""],id:[5,4,1,""],rows:[5,4,1,""],stringify:[5,3,1,""]},"sfftkrw.schema.adapter.SFFVertex":{designation:[5,4,1,""],id:[5,4,1,""],point:[5,3,1,""],x:[5,4,1,""],y:[5,4,1,""],z:[5,4,1,""]},"sfftkrw.schema.adapter.SFFVertexList":{from_hff:[5,3,1,""],num_vertices:[5,3,1,""],vertex_ids:[5,3,1,""]},"sfftkrw.schema.adapter.SFFVolume":{cols:[5,4,1,""],from_hff:[5,3,1,""],rows:[5,4,1,""],sections:[5,4,1,""]},"sfftkrw.schema.adapter.SFFVolumeStructure":{voxel_count:[5,3,1,""]},"sfftkrw.schema.base":{SFFAttribute:[5,2,1,""],SFFIndexType:[5,2,1,""],SFFListType:[5,2,1,""],SFFType:[5,2,1,""],SFFTypeError:[5,5,1,""]},"sfftkrw.schema.base.SFFIndexType":{from_gds_type:[5,3,1,""],increment_by:[5,4,1,""],index_attr:[5,4,1,""],index_in_super:[5,4,1,""],reset_id:[5,3,1,""],start_at:[5,4,1,""],update_index:[5,3,1,""]},"sfftkrw.schema.base.SFFListType":{append:[5,3,1,""],clear:[5,3,1,""],copy:[5,3,1,""],extend:[5,3,1,""],from_gds_type:[5,3,1,""],get_by_id:[5,3,1,""],get_ids:[5,3,1,""],insert:[5,3,1,""],iter_attr:[5,4,1,""],pop:[5,3,1,""],remove:[5,3,1,""],reverse:[5,3,1,""],sibling_classes:[5,4,1,""]},"sfftkrw.schema.base.SFFType":{"export":[5,3,1,""],from_gds_type:[5,3,1,""],gds_tag_name:[5,4,1,""],gds_type:[5,4,1,""],iter_attr:[5,4,1,""],repr_args:[5,4,1,""],repr_str:[5,4,1,""],repr_string:[5,4,1,""]},sfftkrw:{__init__:[6,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"],"5":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute","5":"py:exception"},terms:{"0mhussarv19zrbi":2,"0rvx0adhh77cu":2,"0vfurl":2,"0x10bfc66d0":[],"0x10c960dd0":[],"0x10c9c0550":[],"16noz29l300rpesnlfsqncvrivhynoxhnrmv2ebd2oojv4xr5zn1sb6zhzxflghrvv54oihy7end431sw":2,"17rvatvb":2,"191k":[],"1re6uc2fcbfagt8t3zd41dl3fbk3jz33eqp2a":2,"1tt":2,"1tvjpzlaw8nj1mhe70":2,"1u5n182f":2,"1v49scrr2u09":2,"1vp":2,"1wvv3x2vklc":2,"1xm3o":2,"255qhn6l":2,"2etvd3z12fbni":2,"2f2lr6pry4":2,"2rrm":2,"2ur6q1y4":2,"2v3lj1vp6lvblwvmqtbem9rj31qnmrp9f7xjysovkxl40fufj5kyfnkpf":2,"2vg29s9f7ym":2,"2xg5rb9o":2,"2z7m8cvmhi6":2,"381k":[],"399qx":2,"39j4hhv2e":2,"3a3d":2,"3dnerz9yvmd2z06v1v7q8ysgsbbr91stijy65":2,"3ja8":2,"3qs4sa9wj5vg5zz4vi":2,"3vwaf":2,"3x1":[],"3x3":[],"42zvib1na3fwnhcefkfvup33cpsxfk":2,"48h73xjkta2kpvcbmn3kmti":2,"4v28bkdl54vxzv":2,"4wl3uu7et":2,"4x4":[],"4ztjhffun3ze11jzh3voqhx7o5ghnl3no4m57zxvn7yz8548rlfzklzv7gdjmyglndzn2ktc7":2,"52hrtzq2rwz1jw357bs9rtpfnd8zxc1ix3vstbr71obplfdbv1lnnqr1yrdhbev09tzeaw":2,"5cods36t99xrqs3ppv947c8kfdcomp4vvfl8":2,"5idq9us3ve9dxkfn6tjh7o63es6mqmorxesqa695kd9e2wfnrnm5":2,"5lcaqk1ylt48vmtu21ztmennzue0fw6n3vcuwvv2hjmrzsung":2,"5m9iqr7rrpp1p1ldcx":2,"5rcbzffktudzumwxpx3rrff9zyoyb49u3fa9w32xhgv":2,"5thj3bn9hxn65vakax13kttjshxmgnzi":2,"5tjf2uz":2,"5vfxxx4inak5nymysxp":2,"6rfh9l":2,"6vgv6c6dovg9df":2,"7189vnze7":2,"78vvffi655uqzp36wpplpzx1":2,"7tye":2,"7vi3kieusaz":2,"7xdxt":2,"7zpone3o8phqx":2,"81rc199le5sn4gmf1g7ndldpzoqv6vpp7r4udqnxr46x7rn5x5uqr3kp98z3zjrnjsefxdutqxf6zbvjbmtp8l0y81zrst1ris9ux5vb16vbcxsioipp2a":2,"8kemd":2,"8lbvrfh1tpdyw":2,"8m4z7zx752n":2,"8tfw77ubx47g5ur2qrwan70yzlf7xjpzrvnc1cdvk097pml3ez":2,"8u49ohsjpjjevzoun6r1latb32":2,"8x3138dir64vb6vpqswvgvqszjz0lvwzphsf31dpgp4":2,"8x3btprqxf2kj78rz4wx9vxnynqp9zo":2,"8yj6hndwxjzyb":2,"96k":[],"9amnjyw8bhrrbu5t":2,"9b3e3hwh1kit2biro":2,"9vo7lplrrow6vn8fneln1ht7z":2,"9xow3hmg9c2fme37lob":2,"9zodouplodf4zd7bvnm5judt6vbukhcgomxat":2,"9zz41w976eiosvzurja8zmx1ndh3lttrr6wb1pi3z":2,"\u03b2":2,"byte":[1,5],"case":5,"class":[2,7],"default":[0,1,4,5,7],"export":[0,3,5,7],"final":2,"float":2,"function":[0,1,5,7],"gr\u00fcnewald":7,"import":[2,5,7],"int":[1,5],"jos\u00e9":7,"long":5,"new":[2,5],"null":0,"return":[1,5],"short":5,"static":5,"true":[1,5],"try":5,"var":5,"while":0,Are:[],For:[5,7],IDs:5,The:[1,3,4,7],Then:[3,7],There:0,These:2,Use:7,Used:7,Using:3,With:[],__future__:2,__temp_fil:[],__temp_file_ref:[],_arg:[1,5],_bin:[],_io:1,_kwarg:5,_local:5,_prep:[],aabbcc:1,abil:[],about:[5,7],abov:[2,5],access:5,accident:[],accomplish:[0,5],accord:[],across:5,act:5,action:5,actual:2,ad9aojz0r9ac2fhop:2,adapt:[2,6,7],add:[1,2],add_arg:1,add_complex:2,add_external_refer:2,add_externalrefer:[],add_lattic:2,add_macromolecul:2,add_mesh:2,add_polygon:2,add_seg:2,add_shap:2,add_to_seg:[],add_transform:2,add_vertex:2,added:2,adding:7,addit:5,addition:[],address:7,affect:[],after:2,agnost:7,ah3kmc9:2,algorithm:[],alia:5,align:[],all:[0,1,2,4,5,7],allow:[0,5,7],alongsid:5,alpha:[2,5],alphabet:[],also:[0,7],altern:[],alun:7,am_seg:[],amino:2,amirahxsurfac:[],amirahypersurfacesegment:[],amiramesh:[],amirameshsegment:[],an82vc0ee0pbc4my3xtvb5rqy8irgtgf:2,ani:[0,1,4,5,7],annot:[0,5,7],annotated_sff:2,annotation_onli:5,anoth:[2,5],anyth:[],aozrcs8xv51y5qbyl9nldzdfwtvm9or:2,ap9bjwb:2,apach:7,api:[2,5,7],appear:5,append:[2,5],appli:[0,5],applic:[2,7],aqd6rbrtlip4gn:2,archiv:5,ardan:7,arg:[1,5],argpars:1,argument:[0,1,2,4,5],argumentpars:1,arrai:[2,5],arrang:2,articl:7,as_hff:5,as_json:5,as_seg:[],ascii:1,ascii_b:1,ashton:7,aspect:2,assembl:2,associ:[2,5],assum:[1,5],atom:2,attempt:[],attribut:[2,5,7],augkcv0xrj1r322fqjnxrnvo5lzthyn3njg1ncvrrk0gu9g5ucaqeam7xcdkexixmpflxflu:2,auto:7,auxiliari:[],auxilliari:0,avail:7,background:2,baff5zt:2,bank:7,base64:[2,5],base:6,basic:7,bczhduf8145:2,becaus:[2,5],been:2,begin:[1,5],behaviour:5,being:[1,5],below:5,bernard:7,best:[],better:[],between:[0,7],bh71wgz3:2,big:[2,5],binaris:[],binlist2:2,binlist:2,binmap:[],bioann:2,bioinformat:7,biolog:5,biologi:7,biological_annot:[2,5],biologicalannot:5,bj31hsk:2,blue:[2,5],bool:[1,5],both:[],bottom:5,bottom_radiu:5,bottomradiu:2,bound:[2,5],bounding_box:[2,5],boundingbox:5,box:[2,5],bp61hn3ozpjphjj:2,bpsuycxxo6eol7ibxhxdusjc:2,brace:5,brandt:7,bridg:7,bridget:7,brief:[5,7],browser:[],build:7,built:5,butcher:7,button:[],byte_seq:5,bzstlzd:2,c6v6:2,c7txmlggowloctznhvyqlw23gnol:2,c7volvfbz8zs7ngwr292plevdx6qakutxpnmgv:2,c8ba6vp5:2,c98y5b5tdl46y42touvsjs4otx17eeybv9aqpem871xvl9vjrnnwyq17:2,call:5,can:[0,1,2,5,7],carazo:7,carragh:7,carri:7,carzaniga:7,cast:5,ccp4:[],cellular:7,central:2,cerevisia:2,certain:5,challeng:7,chang:[3,5,7],channel:[1,2,5],charact:1,check:1,checkout:[3,7],child:2,children:5,chiu:7,choic:2,chosen:[],chromatin:2,chunk:4,cite:7,cl57kwdq:2,classmethod:5,clear:5,clear_annot:5,click:[],close:1,cls:5,code:7,col:[2,5],collect:[1,5],collinson:7,colour:[1,5],column:5,com:7,combin:5,command:[1,2,7],commandlin:1,commenc:[],comment:7,commun:7,comp1:2,comp2:2,comp:2,compact:[],compar:0,complet:[2,5],complex:5,complexes_and_macromolecul:[2,5],complexesandmacromolecul:5,complexid:[],compmacr:2,compon:2,compos:[],compress:0,concaten:[],concentr:1,concert:2,cone:[2,5],conf:[],confer:5,config:0,config_nam:[],config_path:0,config_valu:[],configur:5,conform:[],congruent:5,conserv:2,consid:5,consist:[2,7],constrict:2,construct:5,consult:[2,7],contain:[0,2,5],context:7,continu:5,contour:2,contour_level:[],contourlist:[],conveni:[1,5],convers:[0,5],convert:[1,3,5,7],copi:5,copy_annot:5,copyright:7,core:[0,2,3,4,6,7],corei:7,corner:5,correct:[1,5],correspond:[5,7],correspondingli:[],could:[],creat:[0,3,5,7],creation:2,crm7dq3ndrefa4mvzvp6tpi:2,crp5vgnbw7nm0g7lu3mxnno:2,cryo:2,csbubz:2,ctp53h1wfo4mbtcy4dm4ed9uoljdsb9r5xn0fac869smew1vpux63v9ktr4dzunhe2v6m2lnni7srnzsl2hvrk0v:2,cu88fgkjoktsimc1nx1tpaqfxqzu6j7:2,cube:[],cuboid:[2,5],current:[4,5,7],custom:[],cylind:[2,5],czxn6o95mfng:2,da9qwn8r0tfa:2,data:[0,2,5],dataset:0,date:1,david:7,dbunufkrmhmnlenrw:2,decoupl:5,decreas:[],dedic:[],defin:[1,2,5],definit:5,deform:2,del:[],del_not:[],delete_from_seg:[],delimit:5,denot:5,depend:[5,7],deriv:5,describ:[0,2,5],descript:[0,2,5,7],descriptor:[2,3],design:[2,5,7],detail:[2,3,5],detect:7,determin:[0,5],dev0:2,dev3:2,develop:3,df6xs7q2urizfqe4yt1zzie9kqetlxuq:2,dh3dwo1x165d2zzd:2,dialogu:[],diamet:[2,5],dict:1,dictionari:[1,5],differ:5,dimens:[2,5],dimension:7,directli:5,directori:0,disc:5,discuss:7,disk:2,dismiss:[],displai:[0,1,5],distort:[],djsduu9pdarblr:2,dna:2,doc:7,document:[5,7],doe:[1,5],doing:1,dolor:[0,2],domain:2,done:0,doubl:2,down:[],download:[],drop:0,ds0kcvrbxp79j4xjby:2,due:[],duplex:2,dure:[0,2],dyf:2,e092o0evrord6sr2lu3pv5rt2lu82hn0sprt05b:2,e2b55xzsrtvnmjj17:2,each:[2,5],easi:7,easier:5,easili:5,eat4ah7z2mg98dmvx1pm9m9:2,ebi:[2,7],edit_in_seg:[],edit_not:[],effect:[],effici:[],either:[5,7],ejyn19ko48qorff6:2,ekkdspk1n9cyvi:2,electron:[2,7],elif:7,elimin:[],ellipsoid:[2,5],elmol69svvlkpetn81810k:2,embed:[],embl:7,emd_1014:2,emd_6338:2,emdb:[3,5],emdb_sff:5,emdb_stat:7,emma:7,emmkrfnsbe6ctcyp71ktq2zfw5c5utx:2,empiar:7,empti:5,enabl:[0,5],encapsul:5,encod:[1,2,5],end:1,endian:[2,5],ensur:[0,1,5],entiti:5,entri:2,eqt:2,equal:[],equival:0,erp7xt7pfs9r3xth5cwky583fdt6:2,error:[0,5],etc:5,eukaryot:2,european:7,even:0,eventu:[],everi:[2,5],exampl:[5,7],except:[0,5,7],exclud:[0,5],exclus:7,exist:[5,7],exit:[0,4],exlus:[],expect:[],experi:7,explicit:[],express:7,ext:[],extend:[2,5,7],extens:[0,2,5],extern:5,external_refer:[2,5],externalrefer:2,externalreferenceid:[],extra:5,extract:5,extref:2,f1xxq1gs0euex3lrd:2,f2r:2,factor:2,fail:0,fallback:[],fals:[0,1,4,5],far:2,fashion:2,featur:2,fefxxb1:2,fewer:7,fiction:5,field:[0,2],file1:[],file2:[],file3:[],file:[1,3,5,7],file_:[],file_bin:[],file_doubl:[],file_prep:[],file_transform:[],file_tx:[],filenam:5,filetyp:0,fill:5,filter:[],find:[],first:[1,2,5],fit:2,flag:[],flank:2,float32:[2,5],float64:5,follow:[0,5,7],fom:5,form:2,format:[1,2,3,4,5,7],found:5,four:2,fq08b0otavjfefzw:2,fqcyedisnrdhnndcubmvgwys3m:2,fraction:[],free:[5,7],freeli:[],frhlj:2,fri:[],from:[0,1,2,5,7],from_arrai:5,from_byt:5,from_fil:[0,4,5,7],from_gds_typ:5,from_hff:5,from_id:5,from_json:5,frtxvyy1z2nm1pcep7rivlqflepx2zo22vvok1x3weqx6vtxi76bvjfhi0fbg56trwpexpmvzvy59zhfkrrxl:2,fulfil:5,full:[4,7],fzr9nu65l1j:2,g0blivxud:2,gate:2,gault:7,gds_tag_nam:5,gds_type:5,gener:[2,5],geometr:[0,5],get:[1,3,5],get_by_id:[2,5],get_data:[],get_id:[2,5],get_path:1,get_printable_ascii_str:1,github:7,given:[1,5],global:5,global_external_refer:5,grant:7,graphic:[],greater:[],green:[2,5],group:[5,7],guarante:5,guid:[0,7],h54qbtrv5r15oxgv51qjledah:2,h5py:5,hairpin:2,handl:[2,5,7],handle_convert:1,handler:1,has:[2,5],hashabl:1,have:[2,5,7],hdf5:[0,2,5,7],header:2,heavi:1,hecksel:7,height:[2,5],helicas:2,help:[0,1,4,5],henc:[],henderson:7,here:[2,5],heterohexamer:2,hex:1,hexam:2,heymann:7,hff:[0,2,5,7],hff_data:5,hill:7,hit:[],hns6c:2,hoc:[],hold:[],hope:[],host:5,houf3tnsobyw16tq3bpzn:2,how:[0,2,5,7],howev:[5,7],html:7,http:[2,7],hundr:[],ideal:0,ident:2,identifi:[],ids:5,ieof:[],ignor:5,ihg7y1qfphr:2,imag:[],imat:[],imod:4,imodmesh:[],imodsegment:[],implement:5,impli:5,improv:7,inact:2,incl_dat:1,includ:[1,5],incorpor:[],increment:5,increment_bi:5,indent:5,indent_width:5,independ:2,index:[2,3,5],index_attr:5,index_in_sup:5,indic:5,individu:[0,2,5],infer:[2,5],infil:[],inform:[0,2,5],inherit:5,input:[],insert:[0,5],insid:5,inspector:[],inst:5,instal:[],instanc:5,instanti:5,instead:1,institut:7,int16:5,int32:5,int64:5,int8:5,integ:[],integr:[2,5,7],interact:2,interdigit:2,interest:[],interfac:2,interior:2,interv:[1,2],interven:2,introduct:3,invok:[],ip1p78n81lp:2,ipsum:[0,2],iri1:[],iri2:[],iri:5,iroqmvnvmsot3qo:2,irviu3uc:2,item:[1,5],iter:[1,5],iter_attr:5,its:[2,5],iu21fvqi7ehh:2,jan:[],jcw:2,jegvtoun8yhpl77l90r5v2v:2,jensen:7,jm30wq:2,join:2,jrx5lntwz1n:2,jsf:2,json:[0,2,5,7],json_fil:5,k0cyhfwrrwne5p7:2,kai:7,kei:[1,5],keyword:[1,5],kind:[],kink:2,klass:5,know:[],kseqhpfmg8ngt85mztal:2,kvvjvdy:2,kwarg:[1,5],kx1jvvxzjvrz4o8qa9xbc3rizwx3pefoosupqmwal7kj2ttzi2lc23yn5i2vs3jk:2,l37bb:2,l43a:2,l5mxed:2,label:[2,5],lack:2,larg:0,larger:[],last:5,lattic:[2,5],lattice2:2,lattice_id:5,latticeid:2,launch:[],lbxlr6vlvocn2jdrvesvgs9c7:2,lczfnfzef5cplbxvrhfvyk7x65p:2,lead:[],least:[],left:[],len:[2,5],length:[2,5],level:[0,2,5],lf3ddvahh9k9en:2,lib:1,licens:2,lift:1,like:[2,5],line:[1,2,7],linux:0,list:[1,4,5],listinfo:7,listserv:7,liter:5,littl:[2,5],lj33q19be:2,lj6y:2,loa77xzcxry3oal87j9ofzb3hmp8mt8rb:2,load:5,loc43md15ytz6xz2rxv3kexwyugm:2,local:[],locat:[2,5],look:[2,3,7],lorem:[0,2],lossless:0,luci:7,lurfyfgxs1sd73bqwn:2,m48z39iyfj2jvdiz7gwtpsv2byk78dt5ws52fl:2,m9elknqc2afxiylxz98uv:2,macr1:2,macr2:2,macr:2,macromolecul:5,macromolecular:7,macromoleculeid:[],macromoleculesandcomplexestyp:5,magic:5,mai:[5,7],mailman:7,main:[0,2,4,5],mainli:2,mainten:2,make:[0,2,5],manag:[5,7],mandatori:0,mani:0,manner:[],map:[0,2],map_seg:[],mapsegment:[],mar:[],march:[],maria:7,mark:[],mask:[],mask_valu:[],matrix:[2,5],maxim:1,maximum:5,mbnw2d7sa1ktc2vvdnzv:2,mbv199ioj:2,mcm2:2,mcm5:2,mcm7:2,mean:7,mechan:2,melt:2,memori:[],menu:[],merg:5,merge_annot:5,mesh:[0,5],meshlist:[0,2,5],messag:[0,4,5],metadata:[3,7],method:[2,5],mfde2by6zr50vl:2,mg68z371sf6shzef14d73:2,microscopi:[2,7],might:[],minichromosom:2,minimum:5,minx:[],miscellan:[2,3,6],mixin:[],mlq:2,mod:4,mod_seg:[],mode:[1,2,5],model:[0,4,5],modifi:1,modread:[],modul:[3,5,6],molecular:7,more:5,most:5,mostli:[],mpy41w:2,mql:2,mrc:0,much:[],multi:0,multifil:[],multipl:[0,5],must:5,mvcnz1irpnu2l:2,my_arg:1,my_output:[],n2u0cqk60z7vml:2,n69ve:2,n9phit:2,naiv:[],name:[1,2,5,7],namespac:1,narrow:2,natur:7,navig:3,ncbitaxon:2,ncbitaxon_559292:2,ndarrai:5,necessari:[],need:[2,5],newlin:1,newmodel:[],next:[2,5],njhlvfzv3nq3wp81omvdnvbxhbcbpf:2,nnylfbek9xtj4q0ylp5nvuenm0gu20sspnlmzc1p:2,no_polygon:2,no_vertic:2,non:[1,5],none:[0,2,5],normal:[2,5],normalis:[1,2],note:[2,4,5],notic:5,now:[2,5],npvq0ffqudg42tj3lukrtqonnvnonv9aj3nx:2,nsxxczapgl98rhe12zrdz7ogznfgpm:2,num_con:5,num_cuboid:5,num_cylind:5,num_ellipsoid:5,num_global_external_refer:5,num_polygon:5,num_tranformation_matric:5,num_vertic:5,number:[1,5],number_of_inst:5,number_ofinst:2,numberofinst:2,numpi:[2,5],nwd7xvmzm:2,nxephv9wtd:2,o3vrm0onefy7mttz:2,obj:5,object:[0,1,3,5],objt:[],obo:2,obo_id1:[],obo_id2:[],obolibrari:2,obtain:5,occupi:[],occur:5,occurr:5,oct:[],offset:2,often:[],onc:2,one:[0,2,4,5,7],onli:[0,4,5,7],ontolog:5,ontology1:[],ontology2:[],opac:5,open:[5,7],oper:[3,5],opjhbr7x3jsj7lppzbc7i:2,option:[0,4,5,7],order:5,ordin:5,org:2,origin:[0,2],other:[0,2,3,5,7],other_seg:5,other_typ:5,othertyp:2,otherwis:[0,5],ought:[],our:2,out:7,outlin:[],output:[2,3,4,5,7],outsid:[],over:5,overcrowd:1,overwrit:[1,5],ovlc6:2,oxnz6mof8wmfcanxdq3fg0c5ei:2,p61x6uxhud3pf:2,packag:[2,3,7],page:3,pair:[2,5],param:[],paramet:[1,5],paraview:[],parent:5,parent_group:5,parent_id:[2,5],parentid:2,pars:1,parse_arg:1,parser:6,part:[],particular:[],partit:[],pass:[0,5],passagewai:2,path:[1,2],patwardhan:7,pdb:2,pdbe:[2,7],per:5,perform:[0,7],persist:[],perus:7,pfex3f3m:2,phase:2,physic:[],pib:2,pid:[],pip:7,pipelin:[],pixel:[],pjexmfzxstysrgsq:2,pkorir:[2,7],place:[2,5],plai:[],pleas:[2,7],plu:[],point:[2,5],polygon:[2,5],polygon_id:5,pop:5,popul:[0,5],posit:[0,1,4,5],possibl:0,powerfulli:[],pqn88rz:2,pr_p38132:2,pre:[],preced:[],prefix:1,prep:[],prepar:7,preparatori:[],present:[],prevent:[],previous:0,primari:[2,3],primarili:0,primary_descriptor:[0,2,5],primarydescriptor:[0,5],primit:[0,5],print:[0,2,5,6],print_dat:1,print_funct:2,print_stat:1,print_str:1,printabl:1,prioriti:[],prioritis:[],process:[0,5],processing_detail:5,processingdetail:[2,5,7],produc:5,program:0,programmeu:5,progress:1,properli:1,properti:5,provid:[0,2,5],ptmahmmt:2,publish:7,purifi:2,purl:2,put:[0,5],pw59jtx6285fs9n1a4z19azwnnmo365qxtxr:2,pycharmproject:2,python2:[],python:[2,7],pzwp452d8p9u3znv9mvfhvmsa4fniwcq33mydj3vvw55w9xubf:2,q59oa:2,qi9fnfj8vp5md8pm4sgem1rqxqz23poo8loe0p:2,qk5pll2i9izvek59agfd9zyw:2,qtnny55ezoxhdtdvy1fvmix5ud:2,qtz:2,question:7,qzr3kndusrx:2,r5lt:2,r6hhqm:2,r7hv9a38:2,r8my9a1fyu49p71qbds0unmtensxq3:2,r9pxirxnf3vsfdo35es97hnutd86nxtp6m:2,radiu:5,raffaella:7,rais:[0,5],randint:2,random:2,random_colour:5,rang:2,rbvz75rf:2,read:[3,5],reader:4,real:[],rec:0,receiv:[5,7],recommend:[],red:[2,5],redefin:1,reduc:[],redunt:0,refer:[1,5],referenc:5,region:[],regul:2,reinforc:2,reinstat:0,rel:[0,2],relat:[],releas:7,relev:7,reli:1,rememb:[],remov:5,render:5,replac:[],replic:2,report:2,repr_arg:5,repr_str:5,repres:[2,5],represent:[2,5],requir:[2,5],reset:5,reset_id:5,respect:[2,5],respons:[],result:[0,7],retriev:5,reus:1,revers:5,rg7fz:2,rgb:1,rgba:[1,2,5],rgba_to_hex:1,rhxzqytw:2,richard:7,right:2,rigid:[],ring:2,robert:7,root:[2,5],rotat:[],roughli:[],row:[2,5],rqemsdgk5sev98pa8b1v7g6exvhxvx:2,rtype:5,run:[0,3,7],rv6l97txvwqblod8r9nmns8uwvp2m3jnhrbcihokm6t:2,ry0a9ypfbh1ib:2,rz5y17:2,s1ecd:2,s1nkgv5sw4xno9nm8:2,s288c:2,s3n8:2,s5wdjdccvro599dmnl:2,s759fm388tde1md9k:2,s7y:2,s8z:2,saccharomyc:2,sai:2,same:[0,5],sampl:5,san:2,saniti:1,sarah:7,save:[],sbz1:2,schema:[2,3,4,6,7],scheme:[],scratch:[2,7],screen:1,search:[1,3],second:2,section:[2,5],see:7,seem:[],seg:[0,2,5,7],seg_fn:2,seg_seg:[],segger:2,seggersegment:[],segment:[0,3,5,7],segmentation_da:7,segmentation_da_doc:7,segmentationa:5,segmentlist:5,segmenttyp:5,segread:[],segtran:7,select:[],sep:0,sequenc:[4,5],sequenti:5,set:5,sete:0,sever:[1,2,5],sf853zezf9:2,sff:[1,3,4,5],sff_seg:5,sff_type:5,sffattribut:[],sffbiologicalannot:[2,5],sffboundingbox:[2,5],sffcomplex:[2,5],sffcomplexesandmacromolecul:[2,5],sffcone:[2,5],sffcuboid:[2,5],sffcylind:[2,5],sffellipsoid:[2,5],sffexternalrefer:[2,5],sffglobalexternalrefer:5,sffindextyp:[],sffitem:5,sfflattic:[2,5],sfflatticelist:[2,5],sfflisttyp:[],sffmacromolecul:[2,5],sffmesh:[2,5],sffmeshlist:[2,5],sffpolygon:[2,5],sffpolygonlist:[2,5],sffrgba:[2,5],sffsegment:[0,2,5,7],sffsegmentlist:[2,5],sffshape:5,sffshapeprimitivelist:[2,5],sffsoftwar:[2,5,7],sfftest:5,sffthreedvolum:[2,5],sfftk:0,sfftkrw:[1,2,6,7],sfftransformationmatrix:[2,5],sfftransformlist:[2,5],sfftype:2,sfftypeerror:5,sffvertex:[2,5],sffvertexlist:[2,5],sffvolum:5,sffvolumeindex:[2,5],sffvolumestructur:[2,5],shallow:5,shape:[0,5],shapeprimitivelist:[0,5],share:5,shell:0,ship:0,shlex:1,should:[0,2,5,7],show:[0,2,4],sibl:5,sibling_class:5,sif9dcarhzyznnvzin7n:2,signifi:5,similar:[],similarli:0,simplenot:[],simplest:[],simpli:7,simplifi:[2,7],singl:[0,2,5],sit:5,site:[],size:[2,5],smooth_decim:[],sns4h9nxoezmwd:2,softwar:[2,5,7],some:[2,5],someth:2,sort:5,sort_kei:5,sourc:[],space:5,special:5,specif:7,specifi:[1,2,3,5,7],staff:[],standard:[],start:[2,3,5],start_at:5,state:0,statist:[],statu:0,stderr:[1,2],stdout:1,step:2,stereolithographi:[],stl:0,stl_seg:[],stlsegment:[],store:[],str:[1,5],straightforward:2,stream:1,strictli:2,string:[1,5],stringifi:5,structur:[1,2,5,7],stuff:1,su8zhnj1f5kjeuqn6pjbb:2,sub:[],subclass:5,subcommand:[],subunit:2,suffix:5,suggest:[2,7],summari:4,sunqzn:2,superclass:5,suppli:[],support:[],supported_format:[],sure:2,surf:[],surf_seg:[],surfac:[2,5],sv9ld1o75u9:2,sw5zjt7ot31odypz7zewgehz4uhzffmt5:2,sxvhxplmptdfdzqce:2,sys:[1,2],t8boxxxc1vfi:2,tabl:[],tag:[0,5],take:[0,5],target:[],task:0,tba:5,tdfdi0f:2,temp:[],temporari:0,tend:[],term:7,termin:[0,2],test:[3,5],test_data:2,test_data_path:2,text:5,textiowrapp:1,textual:7,tgx19lrj6x91k:2,than:[],the_arg:1,thei:[2,5],them:[0,2],themselv:[],therebi:[],therefor:5,thi:[0,1,2,4,5],third:[],this_pars:1,those:5,thousand:[],three:[0,5,7],threedvolum:[0,2,5],threshold:[],through:3,thu:[],tightli:2,tilt:2,time:[],tkfaqttugfam:2,tnf53svzssievj:2,to_id:5,togeth:5,tool:[4,7],toolkit:[2,3],top:0,transfer:[],transform:[2,5],transform_id:5,transformationmatrixtyp:5,transformid:2,transformlist:5,translat:[],treat:[0,1,5],tree:[],tri:[],truncat:[],tue:0,tupl:[1,2,5],twice:[],twist:2,two:[0,2,5],twvnzve286jtfuvmmbu72wxyz33kshcogr9m7v11tfxrlrhpofngl7evixxzvl2t:2,tx_file:[],type:[1,2,5,7],type_:[],typic:[0,5],u96v9v:2,ubc7hp7bx2wtp1b1e7luo:2,udzx2z:2,uint16:5,uint32:[2,5],uint64:5,uint8:5,under:7,underli:2,unicod:[1,5],unit:3,unittest:2,unmodifi:[],unusu:2,updat:5,update_count:5,update_index:5,upon:5,urae8pzvqyzd2tahwtfgn95frlhvq7:2,url:5,usabl:5,usag:[0,1,4],use:[0,5],use_shlex:1,used:[0,2,5,7],useful:[1,2],user:[0,2,5],uses:5,using:[0,1,2,5,7],usr:[],utf:1,util:[2,6,7],utilis:[],utlzruvfp:2,utr47bhh34fnfxcytu3ai51znfxy0xxrqn:2,uucsw29f1tkpezz870vv7zn6y75ry8szu2pvxj4q7qqhn7cet1:2,uvntc:2,uz5xqcmuplsoddzvrbwdrnboj9jr3rgudem5ruclmdffdbzw5y41j5xm:2,v9f7vnqbjz30xvbggfzzmrycazdz5l5:2,val:[],valid:[0,5],valu:[0,1,2,5],valueerror:0,variabl:[1,5],variou:[2,7],vb9xvnufo1c4dmvcnihbewfdc2wg:2,verbos:[3,4],version:[2,3,5,7],vertex:[2,5],vertex_id:[2,5],vertic:[2,5],vg9o7jxd5qxz7tvoxs4z45jxu:2,vid:[],view:[3,5],vjnwvnnf9l8pltcn9ny:2,vndxlk:2,vol1_valu:2,vol2_valu:2,volum:[0,5],voxel:[2,5],voxel_count:5,vs8:2,vtcxtpffqneskd1ujqyg1wa18a29xdneg7wesmakv9avzla:2,vuwlaohjf:2,w555v25izor4mdd:2,w7usbyfpewl4qz4zm2r3ckz4wx28:2,wah:7,wai:[0,1,3,5],want:[],watersh:[],wb0:2,wbpobz:2,wctypn73bnzd5g9na:2,wczy05g:2,welcom:7,well:[],what:5,when:[0,5,7],whenev:[5,7],where:[4,5],wherebi:[],whether:[1,5],which:[2,5,7],whole:5,whose:0,width:5,within:[],without:[1,5],wiu13djv7:2,wlvy:2,work:[0,2,4,5,7],world:7,would:[],writabl:[],write:[1,2,3,5],written:[],wsj7xvjgph1dp7vr9sxzyjfi:2,www:2,wwwdev:7,wzpd9ziz6df9vvr:2,x1mznsrr9pkz4re2wofqpndsvbcxc2rlf2ur:2,xdb3pxnm8:2,xfv58wnv5:2,xfzfctyjnw48qp2lohogpmn:2,xhromcvvfisl1yrxh5f4di:2,xikfywd7z3gpne6uzu3gzl9vantnel2pke:2,xlmg3v1r1xlvqpv9iou7apfivs6s17h:2,xmax:[2,5],xmd9n5c:2,xmg9pvm3ljs754ct1w2xmwfp6pngz11ay33pdc8vqcf:2,xmin:[2,5],xml:[0,2,5,7],xrang:2,xszqpv2vvwqw6sljax5mef26tqc3pb2wxpt2xup1ht8wgo21mz33iypujjrmhvlup1wwxc2sp18txe73:2,xxpdtezi7pkz1tjvzozwf1:2,xz15c8b:2,y6ps1wedhalj:2,yadz1jf8bbg8n9:2,ybx46z2a:2,yd0z88r93oan33v2f:2,ydaihz9mt:2,yeast:2,yj2:2,ymax:[2,5],ymewtz2hntdwd9tlzylxhvlb2agzli:2,ymin:[2,5],you:7,your:3,yqheul9hr1sztlwdsye3vleazoqb6qt:2,ywsthv:2,z9a3d4vv:2,zejewsaj289ywx8uulij05q670nnp7sby1dx6lr5nv2g22ynniqf3d:2,zero:[],zfyh9pwn6jhryk8u1z1ltvuull9m4r:2,zip:5,zk3js2tedufz7fon8nwe68zvr629:2,zmax:[2,5],zmduh8su:2,zmin:[2,5],zqf1thgjx86x5qz1vtnxq1n78nhnlr3uz4mda3e9axmdgsn6rv1hn3lcp:2,zru5jx3vimyf8vljc:2,zspfdfdbz3xh6hlxhjt6s8zxxlj9c:2,zve:2,zwtqlv33j65ndmruqacaz47p8tt9po83r64zpuzwgfwpnnphfyplu8vrsc3vz:2,zxzht:2,zzxoalh9aa80n:2},titles:["Converting Files To EMDB-SFF","sfftk.core package","Developing with <code class=\"docutils literal notranslate\"><span class=\"pre\">sfftk-rw</span></code>","Welcome to <code class=\"docutils literal notranslate\"><span class=\"pre\">sfftk-rw</span></code>\u2019s documentation!","Miscellaneous Operations Using sfftk-rw","sfftk.schema package","sfftk packages","EMDB-SFF Read/Write Toolkit (<code class=\"docutils literal notranslate\"><span class=\"pre\">sfftk-rw</span></code>)"],titleterms:{"byte":[],"class":5,"default":[],"export":2,"public":7,Adding:2,Are:[],IDs:2,The:[0,2,5],Use:[],Using:4,adapt:5,all:[],amira:[],amiramesh:[],annot:2,applic:[],avail:[],base:5,bin:[],biolog:2,ccp4:[],chang:0,chunk:[],clear:[],colour:2,command:[],complex:2,configur:[],contact:7,content:[0,2,3,4,7],contour:[],convert:0,core:1,creat:2,data:7,delet:[],descriptor:[0,5],detail:0,develop:[2,7],document:3,edit:[],emdb:[0,2,7],extern:2,file:[0,2,4],flag:0,format:0,get:[2,7],hypersurfac:[],imod:[],indic:3,infix:[],input:[],instal:7,interconvers:[0,7],interfac:7,introduct:[0,2,7],iter:2,level:[],licens:7,list:2,macromolecul:2,map:[],mask:[],mesh:2,metadata:[2,4],miscellan:[1,4],mod:[],model:7,modul:1,multifil:[],navig:2,negat:[],note:[],number:[],object:2,obtain:7,onli:[],oper:[0,4],option:[],origin:[],output:0,overwrit:[],packag:[1,5,6],parent:2,parser:1,path:0,per:[],prep:[],primari:0,print:1,print_tool:1,pypi:7,quick:0,read:[2,7],reduct:[],refer:2,run:4,schema:5,seg:[],segger:[],segment:2,set:[0,2],sff:[0,2,7],sffattribut:5,sffindextyp:5,sfflisttyp:5,sfftk:[1,2,3,4,5,6,7],sfftkrw:5,sfftype:5,shape:2,show:[],singl:[],sourc:7,specif:[],specifi:0,start:[0,7],stl:[],store:[],surf:[],synopsi:0,tabl:3,test:4,through:2,todo:0,toolkit:7,transform:[],truncat:[],unit:4,user:7,util:1,valu:[],verbos:0,version:4,view:[2,4,7],volum:2,voxel:[],wai:2,welcom:3,where:[],work:[],write:7,xml:[],your:2}})
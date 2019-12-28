package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"
	"os"

	"text/template"
)

type ObjcMethod struct {
	ClassName                string
	MethodName               string
	ObjCSelf                 string
	ObjCMethodName           string
	ObjCMethodParams         []string
	ObjCMethodParamsLen      int
	ObjCIsClassMethod        bool
	ObjCNeedPrintReturnValue bool
	ObjCReturnType           string
	OnEnterString            string
	OnLeaveString            string
}

func main() {
	pwd, _ := os.Getwd()
	dir := pwd+"/headers/"
	if(len(os.Args)==1 || ""==os.Args[1]){
		fmt.Println("请输入头文件名")
		return
	}
	fileName := os.Args[1]
	headerFile := dir + fileName
	outputFile := pwd+"/script/"+fileName
	if(!exist(headerFile)){
		fmt.Println("头文件不存在")
		return
	}
	fileData, _ := readFile(headerFile)

	jsContent := fetchMethods(string(fileData))
	if len(jsContent) > 0 {
		outputFileName :=strings.Replace(outputFile, ".h", "", 1)+".js"
		err := saveFile(outputFileName, jsContent)
		if(nil==err){
			fmt.Println(outputFileName + " \n脚本已生成")
		}else{
			fmt.Println(err)
		}
	}
}


func exist(filename string) bool {
    _, err := os.Stat(filename)
    return err == nil || os.IsExist(err)
}

func fetchClassName(data string) string {
	classNameRe := regexp.MustCompile(`@interface ([^:\(]+) :?`)
	classNames := classNameRe.FindStringSubmatch(data)
	var className string
	if len(classNames) > 0 {
		//className = strings.Split(classNames[0], ":")[0]
		className = classNames[1]
		//fmt.Println(className)
	}
	//fmt.Println(classNames)
	return className
}

func fetchMethods(data string) string {
	methodNameRe := regexp.MustCompile(`[-+] (.+);`)
	methodNames := methodNameRe.FindAllStringSubmatch(data, -1)
	fridaStringBuilder := strings.Builder{}

	for _, value := range methodNames {
		obj := ObjcMethod{
			ClassName:        fetchClassName(data),
			MethodName:       value[0],
			ObjCMethodName:   formatObjcMethod(value[0]),
			ObjCMethodParams: ObjcMethodParams(value[0]),
			ObjCReturnType:   ObjcReturnType(value[0]),
		}
		obj.ObjCMethodParamsLen = len(obj.ObjCMethodParams)
		obj.ObjCIsClassMethod = ObjcMethodIsPublic(value[0])
		obj.ObjCNeedPrintReturnValue = obj.ObjCReturnType != "void"
		obj.ObjCSelf = "ObjC.Object(args[0])"

		split := strings.Split(obj.ObjCMethodName, ":")
		onEnterStringBuilder := strings.Builder{}
		if obj.ObjCIsClassMethod {
			onEnterStringBuilder.WriteString(" +")
		} else {
			onEnterStringBuilder.WriteString(" -")

		}
		onEnterStringBuilder.WriteString("[")
		onEnterStringBuilder.WriteString(obj.ClassName)
		onEnterStringBuilder.WriteString(" ")

		if obj.ObjCMethodParamsLen > 0 {

			for key, value := range split {
				if len(value) > 0 {
					if key == 0 {
						onEnterStringBuilder.WriteString(value[2:])
					} else {
						onEnterStringBuilder.WriteString("+\" ")
						onEnterStringBuilder.WriteString(value)
					}
					onEnterStringBuilder.WriteString(":\"+")

					//fmt.Println("ObjCMethodName ", obj.ObjCMethodName)
					//fmt.Println("ObjCMethodParams ", strings.Join(obj.ObjCMethodParams, ","))
					//fmt.Println("key ", key)
					//fmt.Println("value ", value)
					//fmt.Println()

					var param = obj.ObjCMethodParams[key]
					if param == "id" {
						onEnterStringBuilder.WriteString("ObjC.Object(args[")
						onEnterStringBuilder.WriteString(strconv.Itoa(key + 2))
						onEnterStringBuilder.WriteString("])")

					} else {
						onEnterStringBuilder.WriteString("args[")
						onEnterStringBuilder.WriteString(strconv.Itoa(key + 2))
						onEnterStringBuilder.WriteString("]")
					}

					onEnterStringBuilder.WriteString(" ")
				} else {

				}
			}
			onEnterStringBuilder.WriteString("+\"]")

			//fmt.Println(onEnterStringBuilder.String())

		} else {
			onEnterStringBuilder.WriteString(obj.ObjCMethodName)
			onEnterStringBuilder.WriteString("]")
		}

		obj.OnEnterString = onEnterStringBuilder.String()

		oLeaveStringBuilder := strings.Builder{}
		if obj.ObjCNeedPrintReturnValue {
			oLeaveStringBuilder.WriteString("\"")
			oLeaveStringBuilder.WriteString(obj.ObjCMethodName)

			oLeaveStringBuilder.WriteString(" return:\" + ")
			if obj.ObjCReturnType == "id" {
				oLeaveStringBuilder.WriteString("ObjC.Object(retval)")
			} else {
				oLeaveStringBuilder.WriteString("retval")
			}

			obj.OnLeaveString = oLeaveStringBuilder.String()
		}

		tmpl, err := template.New("test").Parse(fridaTemplate())
		if err != nil {
			panic(err)
		}

		var tmplBytes bytes.Buffer

		err = tmpl.Execute(&tmplBytes, obj)
		if err != nil {
			panic(err)
		}
		fridaStringBuilder.WriteString(tmplBytes.String())

	}

	return fridaStringBuilder.String()
}

func readFile(fileName string) (data []byte, err error) {
	data, err = ioutil.ReadFile(fileName)
	return data, err
}

func saveFile(fileName string,data string)(err error){
	tempData, _ := readFile("./template/template.js")
	result := bytesCombine(tempData, []byte(data))
	err = ioutil.WriteFile(fileName, []byte(result), 0644)
	return err
}

func writeFile(fileName string, data string) (err error) {
	err = ioutil.WriteFile(fileName+".js", []byte(data), 0644)
	return err
}

func bytesCombine(pBytes ...[]byte) []byte {
    return bytes.Join(pBytes, []byte(""))
}

func formatObjcMethod(method string) string {

	re1 := regexp.MustCompile(`: ?(\(\w+ ?\w+ ?.?.?.?.?.?\)\w+)`)
	re2 := regexp.MustCompile(`- [^\)]+\)`)
	re3 := regexp.MustCompile(`\+ [^\)]+\)`)

	method = re2.ReplaceAllString(re1.ReplaceAllString(method, ":"), "- ")
	method = re3.ReplaceAllString(method, "+ ")
	method = strings.ReplaceAll(method, ": ", ":")
	method = strings.ReplaceAll(method, ";", "")

	return method
}

func ObjcMethodParams(method string) []string {
	re := regexp.MustCompile(`: ?\((\w+ ?\w+ ?.?.??.?.?)\)`)
	stringSubmatch := re.FindAllStringSubmatch(method, -1)
	params := []string{}

	for _, value := range stringSubmatch {
		params = append(params, value[1])
	}

	return params
}

func ObjcMethodIsPublic(method string) bool {
	return strings.HasPrefix(method, "+ ")
}

func ObjcReturnType(method string) string {
	re := regexp.MustCompile(`[+-] \(([^\)]+)`)
	stringSubmatch := re.FindStringSubmatch(method)

	return stringSubmatch[1]
}

func fridaTemplate() string {
	return `
Interceptor.attach(ObjC.classes.{{.ClassName}}["{{.ObjCMethodName}}"].implementation, {
 onEnter: function(args) {
  _print(this,{{if .ObjCIsClassMethod}}"{{.OnEnterString}}"{{- else}}{{.ObjCSelf}} + "{{.OnEnterString}}" {{- end}});
},
 onLeave: function(retval) {
{{if .ObjCNeedPrintReturnValue}}
  _print(this,{{.OnLeaveString}});
{{- end}}
  }
});

`
}

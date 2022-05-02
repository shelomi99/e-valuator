import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  ROOT_URL = 'http://localhost:5000';
  private evaluationResults: any;
  private showSpinner: boolean = false;

  setData(data:any){
    this.evaluationResults = data;
  }

  getData():any{
    return this.evaluationResults;
  }

  setIsShowSpinner(value: boolean) {
    this.showSpinner = value;
  }
  getIsShowSpinner(): boolean {
    return this.showSpinner;
  }

  constructor(private http: HttpClient) { }

  send_get_request(id: number, questionNumber: number, question: string, marks: number, modelAnswer: string, studentAnswer: string, keywords: any){
    return this.http.get(
      this.ROOT_URL + '?id=' + id + '&questionNumber=' + questionNumber + '&question=' + question + '&marks=' + marks +
      '&modelAnswer=' + modelAnswer + '&studentAnswer=' + studentAnswer + '&keywords=' + keywords, {responseType: 'text'}
    )
  }

  add_result_get_request(studentId: number, questionNumber: number, question: string, givenMarks: number, marksAllocated: string){
    return this.http.get(
      this.ROOT_URL + '/add' + '?id=' + studentId + '&questionNumber=' + questionNumber + '&question=' + question + '&givenMarks=' + givenMarks +
      '&marksAllocated=' + marksAllocated, {responseType: 'text'}
    )
  }

  get_ids_request(){
    return this.http.get(
      this.ROOT_URL + '/get' , {responseType: 'json'}
    )
  }

  get_results_request(studentId: number){
    return this.http.get(
      this.ROOT_URL + '/get-marks' + '?id=' + studentId  , {responseType: 'text'}
    )
  }
}

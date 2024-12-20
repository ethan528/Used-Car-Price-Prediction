import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';

import 'package:flutter_todo_app/utils/constants.dart';

class DatabaseUtil {
  final fireStore = FirebaseFirestore.instance;
  final currentUserUid = FirebaseAuth.instance.currentUser!.uid;

  addTask(Map<String, String> data) async {
    DocumentReference docRef = await fireStore
        .collection(FirebaseConstants.pathUserCollection)
        .doc(currentUserUid)
        .collection(FirebaseConstants.pathTasksCollection)
        .add(data);

    String taskId = docRef.id;
    await docRef.update(
      {'id': taskId},
    );
  }

  readTask(userId) {
    return fireStore
        .collection(FirebaseConstants.pathUserCollection)
        .doc(currentUserUid)
        .collection(FirebaseConstants.pathTasksCollection)
        .snapshots();
  }

  updateTask(String taskId, Map<String, String> data) {
    return fireStore
        .collection(FirebaseConstants.pathUserCollection)
        .doc(currentUserUid)
        .collection(FirebaseConstants.pathTasksCollection)
        .doc(taskId)
        .update(data)
        .then(
          (_) => Fluttertoast.showToast(
              msg: "Task updated successfully",
              toastLength: Toast.LENGTH_LONG,
              gravity: ToastGravity.SNACKBAR,
              backgroundColor: Colors.black54,
              textColor: Colors.white,
              fontSize: 14.0),
        )
        .catchError(
          (error) => Fluttertoast.showToast(
              msg: "Failed: $error",
              toastLength: Toast.LENGTH_SHORT,
              gravity: ToastGravity.SNACKBAR,
              backgroundColor: Colors.black54,
              textColor: Colors.white,
              fontSize: 14.0),
        );
  }

  deleteTask() {
    return fireStore
        .collection(FirebaseConstants.pathUserCollection)
        .doc(currentUserUid)
        .collection(FirebaseConstants.pathTasksCollection);
  }
}

//
//  Parameter.swift
//  FlowerSDK
//
//  Created by Daniel Nugraha on 09.01.22.
//

import Foundation
import NumPySupport
import PythonSupport
import PythonKit
import CoreML
import NIOCore
import NIOPosix

@available(iOS 14.0, *)
public class ParameterConverter {
    private var np: PythonObject?
    
    private static let appDirectory = FileManager.default.urls(for: .applicationSupportDirectory,
                                                               in: .userDomainMask).first!
    /// The permanent location of the numpyArray.
    private var numpyArrayUrl = appDirectory.appendingPathComponent("numpyArray.npy")
    private let group: EventLoopGroup
    
    public static let shared = ParameterConverter()
    
    private init() {
        group = MultiThreadedEventLoopGroup(numberOfThreads: 1)
        
        let future = group.next().submit {
            PythonSupport.initialize()
            NumPySupport.sitePackagesURL.insertPythonPath()
            self.np = Python.import("numpy")
        }
        
        do {
            try future.wait()
        } catch let error {
            print(error)
        }
    }
    
    private func multiArrayToNumpy(multiArray: MLMultiArray) -> PythonObject? {
        let pointer = try! UnsafeBufferPointer<Float>(multiArray)
        let array = pointer.compactMap{$0}
        let shape = multiArray.shape.map { Int16(truncating: $0) }
        let filteredShape = shape.filter { $0 > 1 }
        return array.makeNumpyArray().reshape(filteredShape)
    }
    
    private func numpyToData(numpy: PythonObject) -> Data? {
        guard np != nil else {
            return nil
        }
        
        guard Python.isinstance(numpy, np?.ndarray) == true else {
            return nil
        }
        
        let fileManager = FileManager.default
        if fileManager.fileExists(atPath: numpyArrayUrl.path) {
            try? fileManager.removeItem(at: numpyArrayUrl)
        }
        
        np?.save(numpyArrayUrl.path, numpy)
        return try? Data(contentsOf: numpyArrayUrl)
    }
    
    private func dataToNumpy(data: Data) -> PythonObject? {
        guard np != nil else {
            return nil
        }
        
        let fileManager = FileManager.default
        if fileManager.fileExists(atPath: numpyArrayUrl.path) {
            try? fileManager.removeItem(at: numpyArrayUrl)
        }
        try? data.write(to: numpyArrayUrl)
        
        return np?.load(numpyArrayUrl.path)
    }
    
    private func numpyToArray(numpy: PythonObject) -> [Float]? {
        guard np != nil else {
            return nil
        }
        
        guard Python.isinstance(numpy, np?.ndarray) == true else {
            return nil
        }
        let flattened = numpy.flatten()
        return Array<Float>(numpy: flattened)
    }
    
    private func numpyToMultiArray(numpy: PythonObject) -> MLMultiArray? {
        guard np != nil else {
            return nil
        }
        
        guard Python.isinstance(numpy, np?.ndarray) == true else {
            return nil
        }
        
        let pyShape = numpy.__array_interface__["shape"]
        guard let shape = Array<Int>(pyShape) else { return nil }
        let shapeNSNumber = shape.map { NSNumber(value: $0) }
        
        if let swiftArray = numpyToArray(numpy: numpy),
           let multiArray = try? MLMultiArray(shape: shapeNSNumber, dataType: .float) {
            for (index, element) in swiftArray.enumerated() {
                multiArray[index] = NSNumber(value: element)
            }
            return multiArray
        }
        return nil
    }
    
    public func dataToMultiArray(data: Data) -> MLMultiArray? {
        let future = group.next().submit {
            if let numpy = self.dataToNumpy(data: data) {
                return self.numpyToMultiArray(numpy: numpy)
            }
            return nil
        }
        
        do {
            let ret = try future.wait()
            return ret
        } catch let error {
            print(error)
            return nil
        }
        
    }
    
    public func multiArrayToData(multiArray: MLMultiArray) -> Data? {
        let future = group.next().submit {
            if let numpy = self.multiArrayToNumpy(multiArray: multiArray) {
                return self.numpyToData(numpy: numpy)
            }
            return nil
        }
        
        do {
            let ret = try future.wait()
            return ret
        } catch let error {
            print(error)
            return nil
        }
        
    }
    
    public func dataToArray(data: Data) -> [Float]? {
        let future = group.next().submit {
            if let numpy = self.dataToNumpy(data: data) {
                return self.numpyToArray(numpy: numpy)
            }
            return nil
        }
        
        do {
            let ret = try future.wait()
            return ret
        } catch let error {
            print(error)
            return nil
        }
        
    }
    
    public func arrayToData(array: [Float], shape: [Int16]) -> Data? {
        let future = group.next().submit {
            let numpy = array.makeNumpyArray().reshape(shape)
            //print("before shape: \(shape)")
            //print("after shape: \(numpy.shape)")
            return self.numpyToData(numpy: numpy)
        }
        
        do {
            let ret = try future.wait()
            return ret
        } catch let error {
            print(error)
            return nil
        }
    }
}


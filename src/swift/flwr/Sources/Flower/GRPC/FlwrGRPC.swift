//
//  File.swift
//  
//
//  Created by Daniel Nugraha on 16.01.23.
//

import Foundation
import GRPC
import NIOCore

public class FlwrGRPC {
    typealias GRPCResponse = (Flwr_Proto_ClientMessage, Int, Bool)
    
    private static let maxMessageLength: Int = 536870912
    private var bidirectionalStream: BidirectionalStreamingCall<Flwr_Proto_ClientMessage, Flwr_Proto_ServerMessage>? = nil
    
    private let eventLoopGroup: EventLoopGroup
    private let channel: GRPCChannel
    
    let extendedInterceptor: InterceptorExtension?
    
    public init(serverHost: String, serverPort: Int, extendedInterceptor: InterceptorExtension? = nil) {
        self.extendedInterceptor = extendedInterceptor
        
        self.eventLoopGroup = PlatformSupport
            .makeEventLoopGroup(loopCount: 1, networkPreference: .best)
        
        let keepalive = ClientConnectionKeepalive(
          interval: .seconds(1000),
          timeout: .seconds(999),
          permitWithoutCalls: true,
          maximumPingsWithoutData: 0
        )
        
        self.channel = try! GRPCChannelPool.with(
            target: .host(serverHost, port: serverPort),
            transportSecurity: .plaintext,
            eventLoopGroup: eventLoopGroup
        ) {
            // Configure keepalive.
            $0.keepalive = keepalive
            $0.maximumReceiveMessageLength = FlwrGRPC.maxMessageLength
        }
    }
    
    public func startFlwrGRPC(client: Client) {
        startFlwrGRPC(client: client) {}
    }
    
    public func startFlwrGRPC(client: Client, completion: @escaping () -> Void) {
        let grpcClient = Flwr_Proto_FlowerServiceNIOClient(channel: channel, interceptors: FlowerInterceptorsFactory(extendedInterceptor: self.extendedInterceptor))
        var callOptions = CallOptions()
        callOptions.customMetadata.add(name: "maxReceiveMessageLength", value: String(FlwrGRPC.maxMessageLength))
        callOptions.customMetadata.add(name: "maxSendMessageLength", value: String(FlwrGRPC.maxMessageLength))
        
        self.bidirectionalStream = grpcClient.join(callOptions: callOptions, handler: { sm in
            do {
                let promise = self.eventLoopGroup
                    .next()
                    .makePromise(of: GRPCResponse.self)
                let response = try handle(client: client, serverMsg: sm)
                promise.succeed(response)
                self.sendResponse(future: promise.futureResult, completion: completion)
            } catch let error {
                print(error)
            }
        })
    }
    
    func sendResponse(future: EventLoopFuture<GRPCResponse>, completion: @escaping () -> Void) {
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                let response = try future.wait()
                _ = self.bidirectionalStream?.sendMessage(response.0)
                if !response.2 {
                    self.closeGRPCConnection(completion: completion)
                }
            } catch let error {
                print(error)
            }
        }
    }

    func closeGRPCConnection(completion: @escaping () -> Void) {
        do {
            print("Closing gRPC bidirectional stream channel")
            try self.channel.close().wait()
            
            print("Closing gRPC event loop group")
            try self.eventLoopGroup.syncShutdownGracefully()
            
            /*if #available(iOS 14.0, *) {
                print("Closing python event loop group")
                ParameterConverter.shared.finalize()
            }*/
            completion()
            
        } catch let error {
            print(error)
        }
    }
    
    public func abortGRPCConnection(completion: @escaping () -> Void) {
        var disconnect = Flwr_Proto_ClientMessage.DisconnectRes()
        disconnect.reason = .powerDisconnected
        var clientMessage = Flwr_Proto_ClientMessage()
        clientMessage.disconnectRes = disconnect
        
        _ = self.bidirectionalStream?.sendMessage(clientMessage)
        closeGRPCConnection(completion: completion)
    }
}
